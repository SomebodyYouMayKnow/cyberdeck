/*
  Cyberdeck enclosure - revision 2
  Units: millimetres. Designed around the saved 226 x 126 mm PCB including
  its eight case-mount lips.

  Export one printable part at a time by changing `part` below.  "assembly" is
  a visual fit-check model; the coloured electronics are envelopes, not parts
  to print.  This model intentionally keeps uncertain connector dimensions as
  editable parameters at the top of the file.
*/

part = "assembly"; // [assembly,base_shell,service_tray,lid,keyboard_frame,esp32_cradle,chameleon_retainer,alfa_cradle,antenna_pivot,battery_hook]
$fn = 48;

// ---- Manufacturing and case geometry ----
wall = 3;
floor_t = 2.4;
clearance = 0.35;
outer = [242,142];
corner_r = 8;
base_h = 42;              // 39.6 mm clear above the removable tray
lid_h = 10;
tray_origin = [4,4];
tray_size = [234,134];
tray_z = 0;               // raise only after a physical Chameleon test

// Saved carrier geometry.  Coordinates are measured from the PCB lower-left.
pcb = [226,126,1.6];
pcb_origin = [8,8];
pcb_inner_offset = [8,8]; // 210 x 110 mm routed board area inside the ear envelope
pcb_standoff_h = 5;
hat_separator_h = 1;
pcb_mounts = [
  [13,13], [210.56,14.4], [13,113], [210.56,113],
  [60.5,4], [165.5,4], [222,35.5], [222,90.5],
  [165.5,122], [60.5,122], [4,90.5], [4,35.5]
];
pi_mounts = [[113.6983,35.5788],[136.6982,35.5788],[113.6983,93.5789],[136.6982,93.5789]];
hat_mounts = [[23.5,66],[81.5,66],[23.5,89],[81.5,89]];
hat_slot = [26.6,85,51.8,8];

// Confirmed planning envelopes.  Change only from a physical measurement.
keyboard_xy = [8,43];
keyboard_size = [88,54];
keyboard_h = 5.0; // M5Stack product-size height; cable/header protrusion is separate
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
chameleon_xy = [138,2];     // 60 x 30 mm PCB reserve, relative to inner-board datum
battery_size = [96,64,26];  // Miady AS-TPB21 manual dimensions; verify the owned bank
chameleon_reserve = [60,30];
alfa_size = [55,25,12];      // provisional AWUS036ACS envelope; measure owned adapter
alfa_xy = [150,70];           // separate cradle only; not reserved on current PCB

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

module board_xy(p) { translate([pcb_origin[0]+pcb_inner_offset[0]+p[0], pcb_origin[1]+pcb_inner_offset[1]+p[1], 0]) children(); }

module tray_xy(p) { translate([pcb_origin[0]+pcb_inner_offset[0]+p[0]-tray_origin[0], pcb_origin[1]+pcb_inner_offset[1]+p[1]-tray_origin[1], 0]) children(); }

module outer_tray_xy(p) { translate([pcb_origin[0]+p[0]-tray_origin[0], pcb_origin[1]+p[1]-tray_origin[1], 0]) children(); }

module pcb_ears_2d() {
  // Exact case-ear outline traced from the current EasyEDA BoardOutline path.
  polygon(points=[
    [8,8],[55.5,8],[55.5,1.5],[57,0],[64,0],[65.5,1.5],[65.5,8],
    [160.5,8],[160.5,1.5],[162,0],[169,0],[170.5,1.5],[170.5,8],[218,8],
    [218,30.5],[224.5,30.5],[226,32],[226,39],[224.5,40.5],[218,40.5],
    [218,85.5],[224.5,85.5],[226,87],[226,94],[224.5,95.5],[218,95.5],
    [218,118],[170.5,118],[170.5,124.5],[169,126],[162,126],[160.5,124.5],[160.5,118],
    [65.5,118],[65.5,124.5],[64,126],[57,126],[55.5,124.5],[55.5,118],[8,118],
    [8,95.5],[1.5,95.5],[0,94],[0,87],[1.5,85.5],[8,85.5],[8,40.5],
    [1.5,40.5],[0,39],[0,32],[1.5,30.5],[8,30.5]
  ]);
}

module pcb_envelope() { linear_extrude(height=pcb[2]) pcb_ears_2d(); }

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
    // Twelve clearances correspond to the live PCB's four corner holes and eight ears.
    for (p=pcb_mounts) outer_tray_xy(p) translate([0,0,-0.1]) m25_hole(floor_t+0.2);
  }
  // PCB support posts align to the saved NPTHs. Use insulating M2.5 hardware/washers.
  for (p=pcb_mounts) outer_tray_xy(p) translate([0,0,floor_t]) standoff(pcb_standoff_h);
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
  frame_xy = [pcb_origin[0]+pcb_inner_offset[0]+keyboard_xy[0]-6, pcb_origin[1]+pcb_inner_offset[1]+keyboard_xy[1]-6];
  frame_size = [keyboard_size[0]+12, keyboard_size[1]+12];
  // A 3 mm base supports the CardKB body; the stepped pocket captures its edges.
  difference() {
    translate([frame_xy[0],frame_xy[1],0]) rr_box(frame_size,3,3);
    translate([frame_xy[0]+6,frame_xy[1]+6,1.15]) rr_box([keyboard_size[0]+2*clearance,keyboard_size[1]+2*clearance],2,2);
    translate([frame_xy[0]+7,frame_xy[1]+7,-0.1]) rr_box([keyboard_size[0]-6,keyboard_size[1]-6],1,1.4);
    // Four M2.5 fastener holes in the printed support's corner ears.
    for (p=[[3.5,3.5],[frame_size[0]-3.5,3.5],[3.5,frame_size[1]-3.5],[frame_size[0]-3.5,frame_size[1]-3.5]])
      translate([frame_xy[0]+p[0],frame_xy[1]+p[1],-0.1]) m25_hole(3.2);
  }
  // Corner ears provide clamp surface without assuming screw holes in the CardKB PCB.
  for (p=[[0,0],[frame_size[0]-7,0],[0,frame_size[1]-7],[frame_size[0]-7,frame_size[1]-7]])
    translate([frame_xy[0]+p[0],frame_xy[1]+p[1],3]) rr_box([7,7],1,2.5);
}

module esp32_cradle() {
  o = [pcb_origin[0]+pcb_inner_offset[0]+lily_xy[0]-4,pcb_origin[1]+pcb_inner_offset[1]+lily_xy[1]-4];
  s = [lily_size[0]+8,lily_size[1]+8];
  difference() {
    translate([o[0],o[1],0]) rr_box(s,4,3);
    translate([pcb_origin[0]+pcb_inner_offset[0]+lily_xy[0]-clearance,pcb_origin[1]+pcb_inner_offset[1]+lily_xy[1]-clearance,-0.1]) rr_box([lily_size[0]+2*clearance,lily_size[1]+2*clearance],2,3.2);
    for (p=[[153,32],[186,32],[153,98],[186,98]]) board_xy(p) translate([0,0,-0.1]) m25_hole(3.2);
  }
  // side rails grip the board edge, leaving the USB-C end and reset/boot controls clear.
  translate([pcb_origin[0]+pcb_inner_offset[0]+lily_xy[0]-1,pcb_origin[1]+pcb_inner_offset[1]+lily_xy[1]+5,3]) cube([1.5,lily_size[1]-10,4]);
  translate([pcb_origin[0]+pcb_inner_offset[0]+lily_xy[0]+lily_size[0]-0.5,pcb_origin[1]+pcb_inner_offset[1]+lily_xy[1]+5,3]) cube([1.5,lily_size[1]-10,4]);
}

module chameleon_retainer() {
  // Fits the 60 x 30 mm document reserve; the 40 x 24 mm device envelope is centered.
  // Four M2.5 holes fasten the printed retainer to matching case bosses, not the PCB.
  s = chameleon_reserve;
  difference() {
    rr_box(s,2,3);
    translate([(s[0]-chameleon_size[0])/2,(s[1]-chameleon_size[1])/2,1])
      rr_box([chameleon_size[0]+0.5,chameleon_size[1]+0.5],1.5,2.2);
    for (p=[[4,4],[s[0]-4,4],[4,s[1]-4],[s[0]-4,s[1]-4]])
      translate([p[0],p[1],-0.1]) m25_hole(3.2);
  }
  // Raised side rails retain the module without covering its face.
  translate([10,3,3]) cube([1.5,24,2]);
  translate([48.5,3,3]) cube([1.5,24,2]);
}

module alfa_cradle() {
  // Provisional standalone retainer: 55 x 25 body estimate, not positioned on the PCB.
  // Confirm adapter shell, antenna connector and USB plug before printing a final cradle.
  s = [alfa_size[0]+10, alfa_size[1]+10];
  difference() {
    rr_box(s,2,3);
    translate([5-clearance,5-clearance,1]) rr_box([alfa_size[0]+2*clearance,alfa_size[1]+2*clearance],1.5,2.2);
    translate([8,8,-0.1]) cube([alfa_size[0]-6,alfa_size[1]-6,1.3]);
    for (p=[[3.5,3.5],[s[0]-3.5,3.5],[3.5,s[1]-3.5],[s[0]-3.5,s[1]-3.5]])
      translate([p[0],p[1],-0.1]) m25_hole(3.2);
  }
  // Open end keeps the USB plug and RP-SMA connector accessible.
  translate([5,5,3]) cube([2,alfa_size[1],3]);
  translate([5+alfa_size[0]-2,5,3]) cube([2,alfa_size[1],3]);
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
  color("seagreen",0.55) translate([pcb_origin[0],pcb_origin[1],floor_t+pcb_standoff_h]) pcb_envelope();
  translate([0,0,floor_t+pcb_standoff_h+pcb[2]]) color("black",0.5) keyboard_frame();
  envelope([pcb_origin[0]+pcb_inner_offset[0]+keyboard_xy[0],pcb_origin[1]+pcb_inner_offset[1]+keyboard_xy[1]],[keyboard_size[0],keyboard_size[1],keyboard_h],floor_t+pcb_standoff_h+pcb[2],"black");
  envelope([pcb_origin[0]+pcb_inner_offset[0]+pi_xy[0],pcb_origin[1]+pcb_inner_offset[1]+pi_xy[1]],[pi_size[0],pi_size[1],8],floor_t+pcb_standoff_h+pcb[2],"forestgreen");
  envelope([pcb_origin[0]+pcb_inner_offset[0]+hat_xy[0],pcb_origin[1]+pcb_inner_offset[1]+hat_xy[1]],[hat_size[0],hat_size[1],12],floor_t+pcb_standoff_h+pcb[2]+hat_separator_h,"royalblue");
  envelope([pcb_origin[0]+pcb_inner_offset[0]+lily_xy[0],pcb_origin[1]+pcb_inner_offset[1]+lily_xy[1]],[lily_size[0],lily_size[1],10],base_h,"purple");
  // The Chameleon reserve is a PCB document outline; this holder is a separate printed part.
  translate([pcb_origin[0]+pcb_inner_offset[0]+chameleon_xy[0],pcb_origin[1]+pcb_inner_offset[1]+chameleon_xy[1],floor_t+pcb_standoff_h+pcb[2]]) color("darkorange",0.7) chameleon_retainer();
  color("orange",0.75) translate([pcb_origin[0]+pcb_inner_offset[0]+chameleon_xy[0]+(chameleon_reserve[0]-chameleon_size[0])/2,
                                  pcb_origin[1]+pcb_inner_offset[1]+chameleon_xy[1]+(chameleon_reserve[1]-chameleon_size[1])/2,
                                  floor_t+pcb_standoff_h+pcb[2]+1]) cube(chameleon_size);
  translate([0,0,base_h]) color("silver",0.45) rotate([-92,0,0]) lid();
}

if (part == "base_shell") base_shell();
else if (part == "service_tray") service_tray();
else if (part == "lid") lid();
else if (part == "keyboard_frame") keyboard_frame();
else if (part == "esp32_cradle") esp32_cradle();
else if (part == "chameleon_retainer") chameleon_retainer();
else if (part == "alfa_cradle") alfa_cradle();
else if (part == "antenna_pivot") antenna_pivot();
else if (part == "battery_hook") battery_hook();
else assembly();
