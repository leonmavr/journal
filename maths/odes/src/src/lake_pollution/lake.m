% Description
%   First order ODE model for the pollution in a lake assuming constant volume
%   y'(t) = f/V * (cin - y)
% Example :
%   y0 = 1e6;
%   timespan = 0:dt:100;
%   [t, y] = ode23(@lake, timespan, y0); plot(t,y);
% Hints:
%   Feel free to change f, cin, and V according to your flow, pollution, and
%   volume data
function yp = lake(t,y)
    f = 1e6*(1 + 6*sin(2*pi*t));
    cin = 3e6;
    V = 28e6;
    yp = f/V * (cin - y);
end