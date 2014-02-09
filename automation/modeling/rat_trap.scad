use <pi_mount.scad>

module RatTrapBox(){
  union() {
    color("blue") cube([240, 150, 2]); 
    FrontFace();
    translate([0, 148, 0]) cube([240, 2, 140]);
  }
}

module FrontFace(){
  difference() {
    cube([240, 2, 140]);
    translate([5, -0.05, 11.5]) cube([230, 2.1, 117]);
  }
}

translate([-120, -75, -70]) RatTrapBox();
