/*
  Cyberdeck enclosure - revision 1
  Units: millimetres.  Designed around the saved 190 x 110 mm carrier PCB.

  Export one printable part at a time by changing `part` below.  "assembly" is
  a visual fit-check model; the coloured electronics are envelopes, not parts
  to print.  This model intentionally keeps uncertain connector dimensions as
  editable parameters at the top of the file.
*/

part = "assembly"; // [assembly,base_shell,service_tray,lid,keyboard_frame,esp32_cradle,chameleon_sled,antenna_pivot,battery_hook]
$fn = 48;

// ---- Manufacturing and case geometry ----
wall = 3;
floor_t = 2.4;
clearance = 0.35;
outer = [204,124];
corner_r = 8;
base_h = 42;              // 39.6 mm clear above the removable tray
lid_h = 10;
tray_origin = [3.4,3.4];
tray_size = [197.2,117.2];
tray_z = 0;               // raise only after a physical Chameleon test

// Saved carrier geometry.  Coordinates are measured from the PCB lower-left.
pcb = [190,110,1.6];
pcb_origin = [7,7];
pcb_standoff_h = 5;
hat_separator_h = 1;
pcb_mounts = [
  [5,5], [55,5], [185,5], [5,105], [99,105], [185,105],
  [5,38], [99,38], [153,32], [186,32], [153,98], [186,98],
  [23.5,66], [81.5,66], [23.5,89], [81.5,89]
];
pi_mounts = [[113.6983,35.5788],[136.6982,35.5788],[113.6983,93.5789],[136.6982,93.5789]];
hat_mounts = [[23.5,66],[81.5,66],[23.5,89],[81.5,89]];
hat_slot = [26.6,85,51.8,8];

// Confirmed planning envelopes.  Change only from a physical measurement.
keyboard_xy = [8,43];
keyboard_size = [88,54];
keyboard_h = 6.3;
pi_xy = [110,32];
pi_size = [30,65];
hat_xy = [20,62.5];
hat_size = [65,30];
lily_xy = [153,32];
lily_size = [25.5,60];
lily_window = [23,47];
lcd_board = [85.01,56.41];
lcd_view = [74,50];       // conservative aperture; verify against the panel
lcd_xy = [16,34];
chameleon_size = [40,24,8]; // adjustable SE3 envelope, not a manufacturer drawing
chameleon_xy = [40,52];     // lives below the service tray, under the keyboard
battery_size = [96,64,26];  // Miady AS-TPB21 manual dimensions; verify the owned bank

// ---- Basic shapes ----
module rr2d(s, r) {
  offset(r=r) offset(delta=-r) square(s, center=false);
}

module rr_box(s, r, h) {
  linear_extrude(height=h) rr2d(s, r);
}

module m25_hole(h=20) {
  cylinder(d=2.8, h=h, center=false);
}

module standoff(h, od=6.2, hole=2.8) {
  difference() {
    cylinder(d=od, h=h);
    translate([0,0,-0.1]) cylinder(d=hole, h=h+0.2);
  }
}

module board_xy(p) { translate([pcb_origin[0]+p[0], pcb_origin[1]+p[1], 0]) children(); }

module tray_xy(p) { translate([pcb_origin[0]+p[0]-tray_origin[0], pcb_origin[1]+p[1]-tray_origin[1], 0]) children(); }

// ---- Base and removable service tray ----
module base_shell() {
  difference() {
    rr_box([outer[0],outer[1]], corner_r, base_h);
    translate([wall,wall,floor_t]) rr_box([outer[0]-2*wall,outer[1]-2*wall], corner_r-wall, base_h);
    // bottom opening lets the service tray and all electronics come out together
    translate([tray_origin[0],tray_origin[1],-0.1]) rr_box(tray_size, corner_r-wall, floor_t+0.2);
    // left-side IR optical opening; the IR module itself is wired, not PCB-mounted.
    translate([-0.1,84,21]) rotate([0,90,0]) cube([10,10,wall+0.2]);
    // right-front rotary encoder panel hole and rectangular peripheral power-switch opening.
    translate([188,108,-0.1]) cylinder(d=7.2,h=base_h+0.2);
    translate([145,103,-0.1]) cube([14,6,base_h+0.2]);
    // cable exits with removable grommets; open only after connector measurement.
    translate([198.8,38,9]) cube([6,18,12]);
    translate([86,-0.1,9]) cube([38,6,12]);
  }
  // tray support rail inside the lower shell
  difference() {
    translate([tray_origin[0]-0.8,tray_origin[1]-0.8,0]) rr_box([tray_size[0]+1.6,tray_size[1]+1.6],corner_r-wall,2.0);
    translate([tray_origin[0]+1.0,tray_origin[1]+1.0,-0.1]) rr_box([tray_size[0]-2.0,tray_size[1]-2.0],corner_r-wall,2.2);
  }
  // Hinge ears.  Use a 2.5 mm steel pin or M2.5 shoulder screw after printing a test pair.
  for (x=[18,95,172]) {
    translate([x,-2,base_h-7]) rotate([90,0,0]) difference() {
      cylinder(d=12,h=6);
      translate([0,0,-0.1]) cylinder(d=2.8,h=6.2);
    }
  }
}

module service_tray() {
  difference() {
    rr_box(tray_size, corner_r-wall, floor_t);
    // continued clearance under the HAT's 2x20 underside connector
    tray_xy([hat_slot[0],hat_slot[1]]) translate([0,0,-0.1]) rr_box([hat_slot[2],hat_slot[3]],1,floor_t+0.2);
    // thin bottom RF window below the Chameleon sled; make it solid if range testing dislikes it.
    translate([chameleon_xy[0]-tray_origin[0]-2,chameleon_xy[1]-tray_origin[1]-2,-0.1]) rr_box([chameleon_size[0]+4,chameleon_size[1]+4],2,1.2);
    // Four countersunk access screws are deliberately outside the carrier PCB outline.
    for (p=[[5,5],[192,5],[5,112],[192,112]]) translate([p[0],p[1],-0.1]) m25_hole(floor_t+0.2);
  }
  // Carrier support posts.  These pass through its non-plated mechanical holes only.
  for (p=pcb_mounts) tray_xy(p) translate([0,0,floor_t]) standoff(pcb_standoff_h);
  // The Pi has a separate set of taller supports above the carrier.
  for (p=pi_mounts) tray_xy(p) translate([0,0,floor_t+pcb_standoff_h+pcb[2]]) standoff(6,5.6,2.6);
  // HAT support posts stop at the carrier; nylon spacers sit between the carrier and HAT.
  for (p=hat_mounts) tray_xy(p) translate([0,0,floor_t+pcb_standoff_h+pcb[2]]) standoff(hat_separator_h,5.6,2.6);
  cable_channels();
}

module cable_channels() {
  // Raised walls guide cables along the rear hinge path and away from screw heads.
  translate([20,6,floor_t]) cube([105,1.8,4]);
  translate([18,8,floor_t]) cube([1.8,35,4]);
  translate([140,8,floor_t]) cube([1.8,28,4]);
  // Tie slots accept small fabric ties; do not crush HDMI or USB cables.
  for (p=[[28,12],[116,12],[148,20]])
    translate([p[0],p[1],floor_t]) difference() {
      cube([8,3,3]);
      translate([2,0.5,-0.1]) cube([4,2.1,3.2]);
    }
}

// ---- User-facing top pieces ----
module keyboard_frame() {
  frame_xy = [pcb_origin[0]+keyboard_xy[0]-4, pcb_origin[1]+keyboard_xy[1]-4];
  frame_size = [keyboard_size[0]+8, keyboard_size[1]+8];
  difference() {
    translate([frame_xy[0],frame_xy[1],0]) rr_box(frame_size,4,3);
    translate([pcb_origin[0]+keyboard_xy[0]-clearance,pcb_origin[1]+keyboard_xy[1]-clearance,-0.1])
      rr_box([keyboard_size[0]+2*clearance,keyboard_size[1]+2*clearance],2,3.2);
    // Two saved carrier frame holes and two case-only front supports.
    for (p=[[5,38],[99,38],[5,105],[99,105]]) board_xy(p) translate([0,0,-0.1]) m25_hole(3.2);
  }
  // lip keeps the keyboard from moving sideways; it does not assume keyboard screw holes.
  for (p=[[pcb_origin[0]+keyboard_xy[0]-1,pcb_origin[1]+keyboard_xy[1]-1],
          [pcb_origin[0]+keyboard_xy[0]+keyboard_size[0]-1,pcb_origin[1]+keyboard_xy[1]-1],
          [pcb_origin[0]+keyboard_xy[0]-1,pcb_origin[1]+keyboard_xy[1]+keyboard_size[1]-1],
          [pcb_origin[0]+keyboard_xy[0]+keyboard_size[0]-1,pcb_origin[1]+keyboard_xy[1]+keyboard_size[1]-1]])
    translate([p[0],p[1],3]) cube([2,2,2]);
}

module esp32_cradle() {
  o = [pcb_origin[0]+lily_xy[0]-4,pcb_origin[1]+lily_xy[1]-4];
  s = [lily_size[0]+8,lily_size[1]+8];
  difference() {
    translate([o[0],o[1],0]) rr_box(s,4,3);
    translate([pcb_origin[0]+lily_xy[0]-clearance,pcb_origin[1]+lily_xy[1]-clearance,-0.1]) rr_box([lily_size[0]+2*clearance,lily_size[1]+2*clearance],2,3.2);
    for (p=[[153,32],[186,32],[153,98],[186,98]]) board_xy(p) translate([0,0,-0.1]) m25_hole(3.2);
  }
  // side rails grip the board edge, leaving the USB-C end and reset/boot controls clear.
  translate([pcb_origin[0]+lily_xy[0]-1,pcb_origin[1]+lily_xy[1]+5,3]) cube([1.5,lily_size[1]-10,4]);
  translate([pcb_origin[0]+lily_xy[0]+lily_size[0]-0.5,pcb_origin[1]+lily_xy[1]+5,3]) cube([1.5,lily_size[1]-10,4]);
}

module chameleon_sled() {
  // Under-tray rail sled.  Mount with VHB or a removable fabric strap after confirming SE3 dimensions.
  s = [chameleon_size[0]+4,chameleon_size[1]+4];
  p = [chameleon_xy[0]-tray_origin[0],chameleon_xy[1]-tray_origin[1]];
  translate([p[0],p[1],0]) difference() {
    rr_box(s,3,2);
    translate([2,2,-0.1]) rr_box([chameleon_size[0],chameleon_size[1]],2,2.2);
  }
  translate([p[0],p[1]+2,2]) cube([2,chameleon_size[1],5]);
  translate([p[0]+chameleon_size[0]+2,p[1]+2,2]) cube([2,chameleon_size[1],5]);
}

// ---- Lid, display and antenna/battery fittings ----
module lid() {
  difference() {
    rr_box(outer,corner_r,lid_h);
    // inner display cavity leaves a 2.2 mm outside skin
    translate([wall,wall,-0.1]) rr_box([outer[0]-2*wall,outer[1]-2*wall],corner_r-wall,lid_h-2.2);
    // HDMI panel viewing aperture and closed-lid ESP32 status window
    translate([lcd_xy[0]+(lcd_board[0]-lcd_view[0])/2,lcd_xy[1]+(lcd_board[1]-lcd_view[1])/2,lid_h-2.3]) rr_box(lcd_view,2,2.5);
    translate([164,38,lid_h-2.3]) rr_box(lily_window,2,2.5);
    // matching hinge ears
    for (x=[18,95,172]) translate([x,-2,-0.1]) rotate([90,0,0]) cylinder(d=2.8,h=6.2);
  }
  // board-edge display retainers: no guessed LCD screw-hole locations.
  for (p=[[lcd_xy[0]-1,lcd_xy[1]+4],[lcd_xy[0]+lcd_board[0]-1,lcd_xy[1]+4],
          [lcd_xy[0]-1,lcd_xy[1]+lcd_board[1]-8],[lcd_xy[0]+lcd_board[0]-1,lcd_xy[1]+lcd_board[1]-8]])
    translate([p[0],p[1],2.2]) cube([3,4,4]);
}

module antenna_pivot() {
  // Printed clevis: use an M2.5 screw/pin to connect this to a separately designed antenna arm.
  // The 6.5 mm bore takes a bulkhead RF pigtail; select connector before printing the arm.
  difference() {
    union() {
      rr_box([18,14],3,4);
      translate([7,5,4]) rotate([90,0,0]) cylinder(d=10,h=5);
    }
    translate([7,5,3.5]) rotate([90,0,0]) cylinder(d=2.8,h=5.2);
    translate([13,8,-0.1]) cylinder(d=6.5,h=4.2);
  }
}

module battery_hook() {
  // One of two configurable hooks for the exterior power bank; use a fabric strap too.
  difference() {
    union() {
      rr_box([18,12],3,4);
      translate([2,2,4]) cube([4,8,18]);
      translate([2,8,18]) cube([14,2,4]);
    }
    translate([9,6,-0.1]) m25_hole(4.2);
  }
}

// ---- visual fit check ----
module envelope(pos,s,h,col) { color(col,0.45) translate([pos[0],pos[1],h]) cube([s[0],s[1],s[2]]); }

module assembly() {
  color("slategray") base_shell();
  color("dimgray") translate([tray_origin[0],tray_origin[1],tray_z]) service_tray();
  color("seagreen",0.55) translate([pcb_origin[0],pcb_origin[1],floor_t+pcb_standoff_h]) cube([pcb[0],pcb[1],pcb[2]]);
  envelope([pcb_origin[0]+keyboard_xy[0],pcb_origin[1]+keyboard_xy[1]],[keyboard_size[0],keyboard_size[1],keyboard_h],base_h,"black");
  envelope([pcb_origin[0]+pi_xy[0],pcb_origin[1]+pi_xy[1]],[pi_size[0],pi_size[1],8],floor_t+pcb_standoff_h+pcb[2],"forestgreen");
  envelope([pcb_origin[0]+hat_xy[0],pcb_origin[1]+hat_xy[1]],[hat_size[0],hat_size[1],12],floor_t+pcb_standoff_h+pcb[2]+hat_separator_h,"royalblue");
  envelope([pcb_origin[0]+lily_xy[0],pcb_origin[1]+lily_xy[1]],[lily_size[0],lily_size[1],10],base_h,"purple");
  color("orange",0.4) translate([chameleon_xy[0],chameleon_xy[1],-chameleon_size[2]]) cube(chameleon_size);
  color("darkorange") translate([tray_origin[0],tray_origin[1],-2]) chameleon_sled();
  translate([0,0,base_h]) color("silver",0.45) rotate([-92,0,0]) lid();
}

if (part == "base_shell") base_shell();
else if (part == "service_tray") service_tray();
else if (part == "lid") lid();
else if (part == "keyboard_frame") keyboard_frame();
else if (part == "esp32_cradle") esp32_cradle();
else if (part == "chameleon_sled") chameleon_sled();
else if (part == "antenna_pivot") antenna_pivot();
else if (part == "battery_hook") battery_hook();
else assembly();
