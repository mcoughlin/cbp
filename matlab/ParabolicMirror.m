%% ParabolicMirror.m 
% C. Stubbs
% Nov 26 2019
 
% computes ray tracing diagram in 2-d for parabolic mirror
 
% use y=x^2/4f to parameterize it where f is focal length 
 
clear all
close all
makeplots=0;
 
thetainmax=300 ; % max incidence angle in arcsec. FOV diameter is twice this.
 
D=130; % mirror dia in mm
 
f=650; % focal length in mm
 
x=-D/2:D/100:D/2;
 
y=x.*x./(4*f); % compute mirror surface
 
slope=x./(2*f); % compute local slope
 
%% compute diffraction limit
thetadiff=0.5E-6/(D/1000);
 
%% FWHM size
xdiff=thetadiff*f;
ticker=0;
 
EE90=[];
EEratio=[];
thetavec=0:thetainmax/20:thetainmax; % for plotting later on
 
for thetain=0:thetainmax/20:thetainmax
    ticker=ticker+1;
%% lauch rays at appropriate angles parabola line
thetainrad=thetain*4.86E-6; 
 
% reflected ray emerges at two times the angle
theta=2*(atan(slope)+thetainrad);
 
% where do they land on focal line? They start at (x,y) and go to (xland,f)
% at an angle theta. So y=mx+yo and f=m*xland+yo and y=x^2/4f and m=tan(theta), therefore
% x^2/4f-m*x=f-m*xland, and
% xland=-(1/m)*(y-m*x-f)=(f-y)/m+x, and m=tan(theta-pi/2)
 
m=tan(theta+pi/2);
 
xland=x-f.*tan(theta);
xland=x-(y-f)./m;
 
%% compute 90 percent encircled energy diameter
centroid=mean(xland);
dx=abs(xland-centroid);
 
EE90(ticker)=2*prctile(dx,90); % this is a diameter
 
EEratio(ticker)=EE90(ticker)/xdiff;
 
%% plots
 
if(makeplots) 
    
figure(10)
histogram(xland,100)
grid on
shg
 
figure(20)
plot(x,xland,'ko')
hold on
% plot([-xdiff/2 -xdiff/2],[f f],'ro')
% hold off
grid on
shg
%%
 
figure(30)
for counter=1:length(x);
    plot([x(counter) xland(counter)],[y(counter) f],'k-')
    hold on
end
grid on
hold off
ylim([f-0.1 f+.1])
xlim([centroid-.1 centroid+.1])
shg
 
figure(40)
for counter=1:length(x);
    plot([x(counter) xland(counter)],[0 f],'k-')
    hold on
end
grid on
hold off
 
shg
 
figure(50)
histogram(dx,100)
hold on
plot([xdiff xdiff],[0 10],'r.-')
hold off
grid on
shg
 
end % end of makeplots loop
 
end  % end of theta loop
 
%%
figure(100)
plot(thetavec/60,EE90*1000,'ko')
hold on
plot([0 thetavec(end)/60], [xdiff*1000 xdiff*1000],'r-')
hold off
xlabel('angle, arcmin','FontSize',14)
ylabel('90% encircled diameter, microns','FontSize',14)
grid on
shg

