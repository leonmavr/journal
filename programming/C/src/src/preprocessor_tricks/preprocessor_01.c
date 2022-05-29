#define MAX(a,b) (((a)>(b))?(a):(b))

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    int a = 0, b = 1;
    int c = MAX(a, b);
    int d = max(a, b);
	printf("%d", c);
}
