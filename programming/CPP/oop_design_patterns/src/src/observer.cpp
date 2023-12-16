#include <iostream>
#include <iomanip>
#include <vector>
#include <deque>
#include <ctime>
#include <cstdlib>
#include <algorithm>
#include <unordered_map>
#include <cmath>
#include <memory>

// forward declaration of subject as it's required by a concrete observer
class StockMarket;

// observer interface
class IObserver {
public:
    virtual void Update(const std::string& stockSymbol, double price) = 0;
    virtual ~IObserver() = default;
};


// Concrete observer A
class Bot: public IObserver {
public:
    Bot(StockMarket& stock_market);
    void Update(const std::string& stockSymbol, double price) override;
    void Predict(const std::string& ticker);
private:
    StockMarket& stock_market_;
    std::unordered_map<std::string, std::deque<double>> price_history_;
    unsigned hist_length_;
};


// subject interface
class ISubject {
public:
    virtual void AttachObserver(std::shared_ptr<IObserver> investor) = 0;
    virtual void DetachObserver(std::shared_ptr<IObserver> investor) = 0;
    virtual void NotifyObservers() = 0;
    virtual ~ISubject() = default;
protected:
    std::vector<std::shared_ptr<IObserver>> observers_;
};


// Concrete subject
class StockMarket : public ISubject {
public:
    StockMarket() = delete;
    StockMarket(std::unordered_map<std::string, double> prices) : pairs_(prices) {}

    void AttachObserver(std::shared_ptr<IObserver> observer) override {
        observers_.push_back(observer);
    }

    void DetachObserver(std::shared_ptr<IObserver> observer) override {
        auto it = std::find(observers_.begin(), observers_.end(), observer);
        if (it != observers_.end())
            observers_.erase(it);
    }

    void NotifyObservers() override {
        for (auto observer : observers_) {
            for (const auto& pair: pairs_) {
                observer->Update(pair.first, pair.second);
            }
        }
    }

    // Simulate a change in the state variable and notify observers
    void UpdatePrices() {
        for (auto& pair: pairs_) {
            auto price = pair.second;
            pair.second += 0.03*price * (rand()%100 - 40)/100;
        }
        NotifyObservers(); // Notify all registered observers
    }

    std::unordered_map<std::string, double> pairs() const {
        return pairs_;
    }

private:
    // state variable of subject - observers are interested in it
    std::unordered_map<std::string, double> pairs_;
};


// Concrete observer B
class Investor: public IObserver {
public:
    Investor(const std::string& name, StockMarket& stock_market) :
        name_(name),
        stock_market_(stock_market) {}
    void Update(const std::string& stockSymbol, double price) override {
        std::cout << "\tInvestor " << name_ << " received update: "
            << stockSymbol << " price is " << std::fixed
            << std::setprecision(1) << price << std::endl;
    }
private:
    std::string name_;
    StockMarket& stock_market_;
};


// Concrete observer B
Bot::Bot(StockMarket& stock_market) :
    stock_market_(stock_market),
    hist_length_(7) {
    for (auto& pair: stock_market_.pairs()) {
        const auto symbol = pair.first;
        const auto price = pair.second;
        std::deque<double> price_copies;
        // push N copies of the current price to each ticker to initialise it
        for (int i = 0; i < hist_length_; ++i)
            price_copies.push_back(price);
        price_history_[symbol] = price_copies;
    }
};

void Bot::Update(const std::string& ticker, double price) {
    std::cout << "\tBot received an update of " << price << " on " <<
    ticker << " ticker" << std::endl;
    auto it = price_history_.find(ticker);
    if (it != price_history_.end()) {
        it->second.pop_front();
        it->second.push_back(price);
    }
}

// predict next price, estimate a technical indicator, suggest buy/sell/hold
void Bot::Predict(const std::string& ticker) {
    std::cout << "\tBot says: " << ticker << "'s tomorrow price will be ";
    auto it = price_history_.find(ticker);
    if (it != price_history_.end()) {
        const auto prices = it->second;
        // "predict" it as the moving average with some
        // positively biased randomness
        double prediction = 0.0;
        for (auto p: prices)
            prediction += p;
        prediction /= prices.size();
        prediction += rand() % 20 - 5;
        // model the RSI by my arbitrary definition 
        std::cout << std::fixed << std::setprecision(2)
                  << prediction << " with RSI = ";
        auto it = std::max_element(prices.begin(), prices.end());
        double max = *it;
        it = std::min_element(prices.begin(), prices.end());
        double min = *it;
        double curr = prices[prices.size() - 1];
        int rsi_perc = static_cast<int>(std::round((curr - min)/(max - min + 0.0001) * 100));
        // simulate an analysis (buy/hold/sell)
        std::string suggestion = "HOLD";
        if (rsi_perc > 70)
            suggestion = "SELL";
        else if (rsi_perc < 30)
            suggestion = "BUY";
        std::cout << rsi_perc << " --> " << suggestion << std::endl;
    }
}


int main() {
    // Create an instance of the subject (stock market)
    std::unordered_map<std::string, double> trading_pairs =
        {{"GOOG", 150}, {"NVDA", 470}, {"AAPL", 180}};
    auto stock_market = StockMarket(trading_pairs);
    // Create instances of observers (investors/bots)
    auto investor = std::make_shared<Investor>("Alice", stock_market);
    auto bot = std::make_shared<Bot>(stock_market);
    // Attach observers to the subject
    stock_market.AttachObserver(investor);
    stock_market.AttachObserver(bot);

    // Simulate changes in stock prices
    srand(static_cast<unsigned>(time(nullptr)));
    constexpr int ndays = 20;
    for (int i = 0; i < ndays; ++i) {
    // wait for some samples to collect some more meaningful data
    if (i > 5) {
            std::cout << "-------- day " << i << " --------" << std::endl;
            stock_market.UpdatePrices();
            for (auto& pair: stock_market.pairs())
                bot->Predict(pair.first);
        }
    }
    // Detach all observers
    stock_market.DetachObserver(investor);
    stock_market.DetachObserver(bot);
    return 0;
}
