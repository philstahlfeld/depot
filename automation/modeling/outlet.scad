module OutletMount(depth, height) {
  translate([0, 0, -depth]){
    cylinder(h=depth+0.1, r=2, $fn=50);
    translate([0, height, 0]) cylinder(h=depth+0.1, r=2, $fn=50);
  }
}

module OutletsMount(n_outlets, spacing, outlet_depth, outlet_height){
  for (x = [0:spacing:(n_outlets - 1) * spacing]){
    translate([x, 0, 0]) OutletMount(depth=outlet_depth, height=outlet_height);
  }
}

rotate([90, 0, 0]) difference(){
  translate([-50, -50, -1]) cube([2000, 2000, 1]);
  color("blue") OutletsMount(n_outlets=4, spacing=47, outlet_depth=2, outlet_height=85);
}
