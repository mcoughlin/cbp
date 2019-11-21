%% CBPsim.m simulates CPB pointing and pupil scanning
% C. Stubbs Oct 12 2019
 
%% the location of the CBP is X0,Y0,Z0, defines z axis, points down
% the input pupil is a disk of diameter D. 
% the pivot point for the pupil is at the origin. This is an invariant. 
% the location of the unrotated pupil is Xp0,Yp0,Zp0, points up
 
% this treatment assumes the two axes of rotation do intersect at a pivot
% point. This is generally true for a balanced telescope, and that point is
% the center of mass of the balanced system 
 
%% initialize
clear all
close all
 
D=1; % pupil diameter in meters
 
% CBP on axis, 2D away
X0=0;
Y0=0;
Z0=2*D;
 
 
% 
% % pupil that pivots about its center:
% Xp0=0;
% Yp0=0;
% Zp0=0; 
 
% alt-az telescope with axis intersection at D/10 above pupil
 
Xp0=0;
Yp0=0;
Zp0=-D/5;
 
% % 
% % % ra-dec telescope with offset RA axis
% Xp0=2*D;
% Yp0=0;
% Zp0=-D/10;
% X0=Xp0; % put CBP above unrotated pupil
 
CBP=[X0; Y0; Z0];
 
% do the 2d problem first, pivot point on z axis, rotate about x axis
 
%% initial position vector for pupil center, col vector
Pupil0=[Xp0; Yp0; Zp0];
 
theta=10;
phi=-10;
%theta=asind(D/(abs(Zp0-Z0))) % use degrees
 
% create rotation matrices about x and z axes
Rx=rotx(theta);
Ry=roty(phi);
 
% rotate x then y
R=Ry*Rx;
 
% compute new location of pupil center
Pupil=R*Pupil0
 
% compute unit normal to surface. CBP has to point parallel to this 
pupilnorm=-Pupil/norm(Pupil)
 
% some scaling of unit normal hits CBP position when it emanates out from
% sourcepoint, so that (all except k are vectors):
% (source point) + k * pupilnorm=CBP, or
% (source point) = CBP - k*pupilnorm AND (sourcepoint) is on the pupil
% plane. So that means ((sourcepoint) - Pupil) dot (pupilnorm)=0. 
% solve for k by plugging in 
% ((CBP-k*pupilnorm)-Pupil) dot (pupilnorm))=0 
 
k=0.001:0.001:1.2*abs(Zp0-Z0);
 
for counter=1:length(k)
    
residual(counter)=dot(((CBP-k(counter)*pupilnorm)-Pupil),pupilnorm);
 
end
 
[foo,minindex]=min(abs(residual));
 
kmin=k(minindex);
 
sourcepoint=CBP-kmin*pupilnorm
 
pupilpoint=sourcepoint-Pupil
 
%% plots
 
figure(10)
plot(k,residual,'ko')
grid on
shg
 
x=linspace(-D/2,D/2,100);
y=x;
 
[X,Y]=meshgrid(x,y);
 
Z=Y.*sind(theta)-X.*sind(phi)+Pupil(3); % put pupil at correct angle and location
X=X+Pupil(1);
Y=Y+Pupil(2);
 
figure(20)
surf(X,Y,Z)
shading interp
grid on
hold on
plot3(CBP(1),CBP(2),CBP(3),'ro')
plot3(pupilpoint(1),pupilpoint(2),pupilpoint(3),'ro')
hold off
xlabel('X')
axis equal
shg
 
 
 

****************************

% CBPsim2.m cylinder-based approach to CBP pointing simulation
% C. Stubbs Oct 13 2019
 
%% the rays that impinge on the pupil at normal incidence form a cylinder with Rinner and Router
% determined by pupil stop radii. Rotating the telescope is the same as
% moving CBP around on the surface of a sphere of radius D_CBP. 
 
clear all
close all
 
DCBP=10 ; % CBP distance from center of rotation, in meters
Router=8.5/2; % LSST pupil from primary
Rinner=4/2; % LSST secondary
 
theta=0:0.01:2*pi;
 
xouter=Router*cos(theta);
youter=Router*sin(theta);
xinner=Rinner*cos(theta);
yinner=Rinner*sin(theta);
 
xcbp=linspace(-DCBP/2,DCBP/2,100);
ycbp=xcbp;
 
[Xcbp,Ycbp]=meshgrid(xcbp,ycbp);
Zcbp=sqrt(DCBP^2-Xcbp.^2-Ycbp.^2);
 
 
%% plots
 
figure(10)
surf(Xcbp,Ycbp,Zcbp)
shading interp
axis equal
grid on
hold on
zslice=linspace(0,DCBP,50);
for counter =1:50
    plot3(xouter,youter,zslice(counter)+0*xouter,'r-')
    plot3(xinner,yinner,zslice(counter)+0*xouter,'r-')
end
hold off
