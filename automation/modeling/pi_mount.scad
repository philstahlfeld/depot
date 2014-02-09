module Standoff(h, r1, r2){
  difference() {
    cylinder(h=h, r=r1, $fn=50);
    cylinder(h=h+0.01, r=r2, $fn=50);
  }
}

module PiMount(){
  cube([85, 56, 1]);
  translate([24.05, 16.55, 1]) Standoff(8, 2, 1.45);
  translate([78.55, 44.95, 1]) Standoff(8, 2, 1.45);
}

module RelayMount(height){
  cube([75, 55, 1]);
  inner = 1.4;
  translate([3, 3, 1]) Standoff(height, 2, inner);
  translate([72, 3, 1]) Standoff(height, 2, inner);
  translate([3, 52, 1]) Standoff(height, 2, inner);
  translate([72, 52, 1]) Standoff(height, 2, inner);
}

module BarrierStripMount(depth){
  translate([5, 11, -depth]) cylinder(h=depth+0.2, r=2, $fn=50);
  translate([120, 11, -depth]) cylinder(h=depth+0.2, r=2, $fn=50);
}

translate([-62.5, -11, 0]) difference(){
  BarrierStripMount(depth=1.5);
}
