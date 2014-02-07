module Standoff(h, r1, r2){
  difference() {
    cylinder(h=h, r=r1);
    cylinder(h=h+0.01, r=r2);
  }
}

module PiMount(){
  cube([85, 56, 1]);
  translate([24.05, 16.55, 1]) Standoff(4, 2, 1.45);
  translate([78.55, 44.95, 1]) Standoff(4, 2, 1.45);
}

color("blue"){
  translate([-42.5, -28, 0]) PiMount();
}
