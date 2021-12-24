% Description:
%   Solves the 1st order ODE dy/dx = f(x,y) using Euler's methods
%
% Example:
%
% f = @(x,y) (x-y)
% [x,y] = myeuler(f, [0,100], 1, 0.001); 
function [x, yest] = myeuler(f,x_domain, y0, h)
  yest = [];
  xmin = x_domain(1);
  xmax = x_domain(length(x_domain));
  x = linspace(xmin, xmax, abs(xmin - xmax)/h);
  yest = [y0];
  for i = 2:length(x)
    yest = [yest yest(i-1) + h * f(x(i-1), yest(i-1))];
  end 
 end
  