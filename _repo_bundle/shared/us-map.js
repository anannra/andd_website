// Simplified continental US map: an SVG path (low-detail, viewBox 0 0 1000 600).
// Plus a roster of ANDD sites (plausible, in Opportunity-Zone-adjacent regions),
// plus helpers to position nodes & draw animated routing arcs.

window.US_VIEWBOX = "0 0 1000 600";

// Hand-sampled low-poly US outline (rough — good enough as backdrop).
window.US_PATH = "M 147,150 L 155,128 L 181,118 L 220,112 L 275,108 L 340,112 L 420,114 L 490,116 L 560,114 L 625,112 L 690,110 L 752,112 L 812,120 L 855,134 L 882,150 L 898,172 L 900,200 L 896,232 L 884,264 L 868,296 L 852,324 L 840,348 L 832,370 L 824,394 L 812,418 L 794,440 L 772,456 L 748,470 L 720,482 L 688,492 L 650,498 L 610,502 L 570,504 L 528,504 L 488,500 L 450,494 L 412,484 L 378,470 L 348,452 L 322,430 L 298,404 L 278,374 L 260,340 L 244,304 L 228,268 L 210,232 L 192,200 L 174,176 L 160,162 Z";

// Nodes: [lon, lat, name, tier]
// tier: "hub" (regional hub) or "edge"
window.ANDD_NODES = [
  // Regional hubs
  {id:'hub-sea', x:180, y:155, name:'Seattle Hub', state:'WA', tier:'hub', pop:'750k'},
  {id:'hub-sjc', x:170, y:310, name:'Oakland Hub', state:'CA', tier:'hub', pop:'1.2M'},
  {id:'hub-phx', x:270, y:380, name:'Phoenix Hub', state:'AZ', tier:'hub', pop:'1.6M'},
  {id:'hub-dal', x:480, y:430, name:'Dallas Hub', state:'TX', tier:'hub', pop:'1.3M'},
  {id:'hub-chi', x:620, y:240, name:'Chicago Hub', state:'IL', tier:'hub', pop:'2.7M'},
  {id:'hub-atl', x:710, y:400, name:'Atlanta Hub', state:'GA', tier:'hub', pop:'500k'},
  {id:'hub-dca', x:830, y:260, name:'Reston Hub', state:'VA', tier:'hub', pop:'63k'},
  {id:'hub-nyc', x:860, y:215, name:'Newark Hub', state:'NJ', tier:'hub', pop:'280k'},
  {id:'hub-mia', x:780, y:525, name:'Miami Hub', state:'FL', tier:'hub', pop:'450k'},

  // Edge nodes — ~42 across OZ-adjacent regions
  {id:'e-01', x:220, y:175, name:'Tacoma', state:'WA', tier:'edge', use:'power'},
  {id:'e-02', x:240, y:220, name:'Portland', state:'OR', tier:'edge', use:'ai'},
  {id:'e-03', x:195, y:265, name:'Medford', state:'OR', tier:'edge', use:'public-safety'},
  {id:'e-04', x:150, y:340, name:'Fresno', state:'CA', tier:'edge', use:'mobility'},
  {id:'e-05', x:205, y:360, name:'Bakersfield', state:'CA', tier:'edge', use:'power'},
  {id:'e-06', x:185, y:410, name:'San Diego', state:'CA', tier:'edge', use:'mobility'},
  {id:'e-07', x:255, y:310, name:'Las Vegas', state:'NV', tier:'edge', use:'civic'},
  {id:'e-08', x:290, y:280, name:'Boise', state:'ID', tier:'edge', use:'power'},
  {id:'e-09', x:340, y:310, name:'Salt Lake', state:'UT', tier:'edge', use:'ai'},
  {id:'e-10', x:320, y:390, name:'Tucson', state:'AZ', tier:'edge', use:'mobility'},
  {id:'e-11', x:380, y:360, name:'Albuquerque', state:'NM', tier:'edge', use:'public-safety'},
  {id:'e-12', x:400, y:310, name:'Denver', state:'CO', tier:'edge', use:'ai'},
  {id:'e-13', x:350, y:275, name:'Cheyenne', state:'WY', tier:'edge', use:'power'},
  {id:'e-14', x:400, y:240, name:'Billings', state:'MT', tier:'edge', use:'power'},
  {id:'e-15', x:470, y:280, name:'Omaha', state:'NE', tier:'edge', use:'health'},
  {id:'e-16', x:510, y:320, name:'Wichita', state:'KS', tier:'edge', use:'civic'},
  {id:'e-17', x:460, y:380, name:'Oklahoma City', state:'OK', tier:'edge', use:'public-safety'},
  {id:'e-18', x:520, y:465, name:'Austin', state:'TX', tier:'edge', use:'depin'},
  {id:'e-19', x:560, y:490, name:'Houston', state:'TX', tier:'edge', use:'power'},
  {id:'e-20', x:440, y:475, name:'San Antonio', state:'TX', tier:'edge', use:'mobility'},
  {id:'e-21', x:400, y:430, name:'El Paso', state:'TX', tier:'edge', use:'public-safety'},
  {id:'e-22', x:585, y:460, name:'Baton Rouge', state:'LA', tier:'edge', use:'power'},
  {id:'e-23', x:620, y:470, name:'New Orleans', state:'LA', tier:'edge', use:'public-safety'},
  {id:'e-24', x:640, y:415, name:'Jackson', state:'MS', tier:'edge', use:'health'},
  {id:'e-25', x:660, y:370, name:'Memphis', state:'TN', tier:'edge', use:'depin'},
  {id:'e-26', x:700, y:340, name:'Nashville', state:'TN', tier:'edge', use:'ai'},
  {id:'e-27', x:665, y:435, name:'Birmingham', state:'AL', tier:'edge', use:'civic'},
  {id:'e-28', x:735, y:425, name:'Savannah', state:'GA', tier:'edge', use:'depin'},
  {id:'e-29', x:780, y:470, name:'Jacksonville', state:'FL', tier:'edge', use:'mobility'},
  {id:'e-30', x:760, y:400, name:'Tampa', state:'FL', tier:'edge', use:'health'},
  {id:'e-31', x:750, y:340, name:'Charleston', state:'SC', tier:'edge', use:'civic'},
  {id:'e-32', x:760, y:310, name:'Charlotte', state:'NC', tier:'edge', use:'ai'},
  {id:'e-33', x:790, y:290, name:'Raleigh', state:'NC', tier:'edge', use:'ai'},
  {id:'e-34', x:800, y:250, name:'Richmond', state:'VA', tier:'edge', use:'civic'},
  {id:'e-35', x:810, y:210, name:'Pittsburgh', state:'PA', tier:'edge', use:'power'},
  {id:'e-36', x:830, y:180, name:'Buffalo', state:'NY', tier:'edge', use:'mobility'},
  {id:'e-37', x:745, y:220, name:'Columbus', state:'OH', tier:'edge', use:'mobility'},
  {id:'e-38', x:700, y:210, name:'Indianapolis', state:'IN', tier:'edge', use:'mobility'},
  {id:'e-39', x:680, y:180, name:'Detroit', state:'MI', tier:'edge', use:'mobility'},
  {id:'e-40', x:600, y:190, name:'Milwaukee', state:'WI', tier:'edge', use:'health'},
  {id:'e-41', x:575, y:150, name:'Minneapolis', state:'MN', tier:'edge', use:'ai'},
  {id:'e-42', x:545, y:210, name:'Des Moines', state:'IA', tier:'edge', use:'civic'},
];

window.INDUSTRIES = [
  {id:'all',          label:'ALL',            color:'#5ee3ff'},
  {id:'mobility',     label:'MOBILITY & V2X',  color:'#5ee3ff'},
  {id:'public-safety',label:'PUBLIC SAFETY',  color:'#ff7a8a'},
  {id:'power',        label:'POWER & UTILITIES', color:'#ffb454'},
  {id:'health',       label:'HEALTHCARE',     color:'#9fe870'},
  {id:'ai',           label:'AI INFERENCE',   color:'#a388ff'},
  {id:'depin',        label:'DePIN',          color:'#5eb8ff'},
  {id:'civic',        label:'SMART CITY',     color:'#c8d4ed'},
];
