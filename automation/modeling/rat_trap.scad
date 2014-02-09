use <outlet.scad>
use <pi_mount.scad>

module RatTrapBox(length=225, width=150, height=120, thickness=3){
  union() {
    BottomFace(length=length, width=width, thickness=thickness); 
    FrontFace(length=length, height=height, thickness=thickness, hole_length=190, hole_height=80);
    RearFace(length=length, height=height, box_width=width, thickness=thickness);
    LeftFace(width=width, height=height, thickness=thickness);
    RightFace(width=width, height=height, thickness=thickness, box_length=length);
  }
}

module FrontFace(length, height, thickness, hole_length, hole_height){
  difference() {
    cube([length, thickness, height]);
    // Make the hole
    translate([(length-hole_length)/2, -0.05, (height-hole_height)/2]) cube([hole_length, thickness+0.1, hole_height]);
    // Make outlet screw ports
    color("blue") translate([(length-141)/2, 0, (height-85)/2]){
      rotate([90, 0, 0]){
        OutletsMount(n_outlets=4, spacing=47, outlet_depth=20, outlet_height=85);
      }
    }
  }
}

module RearFace(length, height, box_width, thickness){
  translate([0, box_width-thickness, 0]){
    difference(){
      cube([length, thickness, height]);
      translate([length/2, -0.05, thickness + 10]){
        rotate([-90, 0, 0]) cylinder(h=thickness+0.1, r=5);
      }
    }
    translate([(length-85)/2 + 85, 0.99, (height-56)/2 + 56 + 10]){
      rotate([-90, 0, 180]) color("green") PiMount();
    }
  }
  
}

module BottomFace(length, width, thickness){
  difference(){
    cube([length, width, thickness]);
    translate([(length-125)/2, 30, thickness]){
      color("orange") BarrierStripMount(depth=2);
    }
  }
  translate([(length-75)/2, (width-55)/2 + 10, thickness]){
    color("red") RelayMount(height=20);
  }
}

module LeftFace(width, height, thickness){
  cube([thickness, width, height]);
}

module RightFace(width, height, thickness, box_length){
  translate([box_length-thickness, 0, 0]){
    cube([thickness, width, height]);
    translate([0, width/2, (height-85)/2]){
      color("purple") rotate([0, -90, 0]) Standoff(h=10, r1=2, r2=1.25);
    }
    translate([0, width/2, height - (height-85)/2]){
      color("purple") rotate([0, -90, 0]) Standoff(h=10, r1=2, r2=1.25);
    }
  }
}

translate([-112.5, -75, -60]) RatTrapBox();
