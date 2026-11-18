import uuid

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Unit Circle & Sinusoidal Signals",
    layout="wide",
)

# Remove Streamlit's default padding/header so the animation fills the page
st.markdown(
    """
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    header[data-testid="stHeader"] {height: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

uid = "unitcircle_" + uuid.uuid4().hex[:8]

html = r"""
<div id="ROOT_ID" class="animation-app">

<style>
#ROOT_ID {
    width:100%;
    max-width:1400px;
    margin:auto;
    padding:clamp(5px, 2vw, 20px);
    box-sizing:border-box;
    font-family:Arial,sans-serif;
    color:#222;
}

#ROOT_ID * {
    box-sizing:border-box;
}

#ROOT_ID h2 {
    text-align:center;
    font-size:clamp(19px, 2.5vw, 28px);
    margin:12px 0 20px;
}

#ROOT_ID .button-row {
    display:flex;
    justify-content:center;
    align-items:center;
    gap:10px;
    flex-wrap:wrap;
    margin:12px auto;
}

#ROOT_ID button {
    color:white;
    padding:11px clamp(12px,2vw,25px);
    border:0;
    border-radius:7px;
    cursor:pointer;
    font-size:clamp(13px,1.5vw,16px);
    font-weight:bold;
    white-space:nowrap;
    touch-action:manipulation;
}

#ROOT_ID button:active {
    transform:scale(0.97);
}

#ROOT_ID .play {background:#198754;}
#ROOT_ID .pause {background:#d99a00;}
#ROOT_ID .reset {background:#555;}
#ROOT_ID .step {background:#1769c2;}

#ROOT_ID .parameters {
    display:flex;
    justify-content:center;
    align-items:center;
    flex-wrap:wrap;
    gap:clamp(15px,3vw,35px);
    margin:25px auto;
}

#ROOT_ID .parameter {
    font-size:clamp(15px,2vw,20px);
    font-weight:bold;
    text-align:center;
}

#ROOT_ID .parameter input {
    display:block;
    width:clamp(100px,15vw,130px);
    margin:7px auto 0;
    padding:9px;
    font-size:clamp(16px,2vw,20px);
    border:1px solid #888;
    border-radius:5px;
    text-align:center;
}

#ROOT_ID .status {
    text-align:center;
    padding:12px 5px;
    font-size:clamp(12px,1.6vw,17px);
    font-weight:bold;
    line-height:1.7;
}

#ROOT_ID .graphs {
    display:flex;
    justify-content:center;
    align-items:flex-start;
    flex-wrap:wrap;
    gap:15px;
    width:100%;
    margin:10px auto;
}

#ROOT_ID .graph {
    display:block;
    height:auto;
    background:white;
    border:1px solid #aaa;
    border-radius:8px;
    max-width:100%;
}

#ROOT_ID .circle {
    width:430px;
    flex:1 1 350px;
    max-width:430px;
}

#ROOT_ID .waves {
    width:600px;
    flex:2 1 480px;
    max-width:600px;
}

/* Dark mode */
#ROOT_ID.dark {
    background:#0d1117;
    color:#e6e6e6;
    border-radius:12px;
}

#ROOT_ID.dark .graph {
    background:#161b22;
    border-color:#444;
}

#ROOT_ID.dark .parameter input {
    background:#0d1117;
    color:#e6e6e6;
    border-color:#555;
}

#ROOT_ID.dark .status {
    color:#e6e6e6;
}

/* Tablet */
@media (max-width:850px) {
    #ROOT_ID .graphs {
        gap:12px;
    }

    #ROOT_ID .circle {
        flex:1 1 300px;
    }

    #ROOT_ID .waves {
        flex:1 1 450px;
    }
}

/* Mobile */
@media (max-width:550px) {
    #ROOT_ID {
        padding:5px;
    }

    #ROOT_ID .graphs {
        flex-direction:column;
        align-items:center;
        gap:12px;
    }

    #ROOT_ID .circle,
    #ROOT_ID .waves {
        width:100%;
        max-width:100%;
        flex:none;
    }

    #ROOT_ID .parameters {
        gap:12px;
        margin:18px auto;
    }

    #ROOT_ID .parameter {
        font-size:15px;
    }

    #ROOT_ID .button-row {
        gap:7px;
    }

    #ROOT_ID button {
        padding:10px 13px;
    }
}
</style>

<h2>Unit Circle & Sinusoidal Signals</h2>

<!-- FIRST ROW: MAIN CONTROLS -->

<div class="button-row">

<button class="play" id="play">▶ PLAY</button>

<button class="pause" id="pause">Ⅱ PAUSE</button>

<button class="reset" id="reset">↺ RESET</button>

<button class="reset" id="theme">🌙 DARK MODE</button>

</div>

<!-- SECOND ROW: STEP CONTROLS -->

<div class="button-row">

<button class="step" id="back">◀ STEP BACK</button>

<button class="step" id="forward">STEP FORWARD ▶</button>

</div>

<!-- INTERACTIVE PARAMETERS -->

<div class="parameters">

<label class="parameter">
Frequency (Hz)
<input id="freq" type="number"
value="1" min="0.1" max="20" step="0.1">
</label>

<label class="parameter">
Time window (s)
<input id="window" type="number"
value="1" min="0.5" max="20" step="0.5">
</label>

<label class="parameter">
Step size (s)
<input id="step" type="number"
value="0.02" min="0.001" max="1" step="0.01">
</label>

</div>

<!-- LIVE INFORMATION -->

<div class="status" id="status">
Time: 0.000 s | Angle: 0° | Frequency: 1 Hz
</div>

<!-- RESPONSIVE GRAPHS -->

<div class="graphs">

<canvas id="circle" class="graph circle"
width="430" height="430"></canvas>

<canvas id="waves" class="graph waves"
width="600" height="450"></canvas>

</div>

<script>
(function(){

const root=document.getElementById("ROOT_ID");

const circle=root.querySelector("#circle");
const waves=root.querySelector("#waves");

const c=circle.getContext("2d");
const w=waves.getContext("2d");

const freq=root.querySelector("#freq");
const win=root.querySelector("#window");
const stepInput=root.querySelector("#step");
const status=root.querySelector("#status");

let time=0;
let playing=false;
let lastTimestamp=null;
let animationID=null;

const cx=215;
const cy=215;
const R=155;

// ======================================
// THEMES (light / dark)
// ======================================

const themes={
    light:{text:"#222",axis:"#999",circle:"#222",radius:"red",
           cosProj:"blue",sinProj:"green",center:"black",
           cos:"#1769c2",sin:"#159447",grid:"#ddd",zero:"#888",
           tick:"#333",axisLine:"#333",
           legendBg:"white",legendBorder:"#aaa"},
    dark:{text:"#e6e6e6",axis:"#8b949e",circle:"#e6e6e6",radius:"#ff5c5c",
          cosProj:"#58a6ff",sinProj:"#3ddc84",center:"#ffffff",
          cos:"#58a6ff",sin:"#3ddc84",grid:"#30363d",zero:"#8b949e",
          tick:"#c9d1d9",axisLine:"#c9d1d9",
          legendBg:"#0d1117",legendBorder:"#555"}
};

let darkMode=!!(window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches);
let T=themes.light;
const themeBtn=root.querySelector("#theme");

function applyTheme(){
    T=darkMode?themes.dark:themes.light;
    root.classList.toggle("dark",darkMode);
    document.body.style.background=darkMode?"#0d1117":"transparent";
    themeBtn.textContent=darkMode?"☀ LIGHT MODE":"🌙 DARK MODE";
}

themeBtn.addEventListener("click",function(){
    darkMode=!darkMode;
    applyTheme();
    render();
});

applyTheme();

// ======================================
// PARAMETERS
// ======================================

function getFrequency(){
    return Math.max(0.01,Number(freq.value)||1);
}

function getStep(){
    return Math.max(0.001,Number(stepInput.value)||0.02);
}

function getWindow(){
    return Math.max(0.1,Number(win.value)||2);
}

// ======================================
// UNIT CIRCLE
// ======================================

function drawCircle(){

    c.clearRect(0,0,430,430);

    const omega=2*Math.PI*getFrequency();
    const angle=omega*time;

    const x=Math.cos(angle);
    const y=Math.sin(angle);

    // Canvas Y-axis is inverted
    const px=cx+R*x;
    const py=cy-R*y;

    // Coordinate axes
    c.strokeStyle=T.axis;
    c.lineWidth=1;

    c.beginPath();
    c.moveTo(25,cy);
    c.lineTo(405,cy);
    c.moveTo(cx,25);
    c.lineTo(cx,405);
    c.stroke();

    // Unit circle
    c.strokeStyle=T.circle;
    c.lineWidth=2;

    c.beginPath();
    c.arc(cx,cy,R,0,2*Math.PI);
    c.stroke();

    // Radius
    c.strokeStyle=T.radius;
    c.lineWidth=3;

    c.beginPath();
    c.moveTo(cx,cy);
    c.lineTo(px,py);
    c.stroke();

    // Cosine projection
    c.strokeStyle=T.cosProj;
    c.setLineDash([6,5]);

    c.beginPath();
    c.moveTo(px,py);
    c.lineTo(px,cy);
    c.stroke();

    // Sine projection
    c.strokeStyle=T.sinProj;

    c.beginPath();
    c.moveTo(px,py);
    c.lineTo(cx,py);
    c.stroke();

    c.setLineDash([]);

    // Moving point
    c.fillStyle=T.radius;
    c.beginPath();
    c.arc(px,py,9,0,2*Math.PI);
    c.fill();

    // Center
    c.fillStyle=T.center;
    c.beginPath();
    c.arc(cx,cy,4,0,2*Math.PI);
    c.fill();

    // Labels
    c.fillStyle=T.text;
    c.font="15px Arial";

    c.fillText("UNIT CIRCLE",145,22);
    c.fillText("0°",cx+R+10,cy+5);
    c.fillText("90°",cx-20,cy-R-10);
    c.fillText("180°",cx-R-45,cy+5);
    c.fillText("270°",cx-25,cy+R+20);

    c.fillStyle=T.radius;
    c.fillText("P",px+12,py-10);

    c.fillStyle=T.cos;
    c.fillText("cos(θ)",px+8,cy+20);

    c.fillStyle=T.sin;
    c.fillText("sin(θ)",cx-65,py-10);

    c.fillStyle="#e67e22";
}

// ======================================
// SINE AND COSINE GRAPH WITH GRID
// ======================================

function drawWaves(){

    const left=65;
    const right=580;
    const top=45;
    const bottom=365;

    const omega=2*Math.PI*getFrequency();
    const windowSize=getWindow();

    const start=Math.max(0,time-windowSize);
    const end=Math.max(windowSize,time);

    function X(t){
        return left+(t-start)/(end-start)*(right-left);
    }

    function Y(v){
        return 205-v*135;
    }

    w.clearRect(0,0,600,450);

    // Vertical time grid
    const rawInterval=(end-start)/8;

    const magnitude=Math.pow(
        10,Math.floor(Math.log10(rawInterval))
    );

    const normalized=rawInterval/magnitude;

    let interval;

    if(normalized<=1) interval=magnitude;
    else if(normalized<=2) interval=2*magnitude;
    else if(normalized<=5) interval=5*magnitude;
    else interval=10*magnitude;

    const firstTick=Math.ceil(start/interval)*interval;

    w.font="11px Arial";
    w.textAlign="center";

    for(let t=firstTick;t<=end+interval*0.001;t+=interval){

        const xx=X(t);

        w.strokeStyle=T.grid;
        w.lineWidth=1;

        w.beginPath();
        w.moveTo(xx,top);
        w.lineTo(xx,bottom);
        w.stroke();

        w.fillStyle=T.tick;
        w.fillText(t.toFixed(2),xx,bottom+18);
    }

    // Horizontal amplitude grid
    const amplitudes=[-1,-0.5,0,0.5,1];

    w.textAlign="right";

    amplitudes.forEach(v=>{

        const yy=Y(v);

        w.strokeStyle=(v===0)?T.zero:T.grid;
        w.lineWidth=(v===0)?1.5:1;

        w.beginPath();
        w.moveTo(left,yy);
        w.lineTo(right,yy);
        w.stroke();

        w.fillStyle=T.tick;
        w.fillText(v.toFixed(1),left-10,yy+4);
    });

    // Axes
    w.strokeStyle=T.axisLine;
    w.lineWidth=1.5;

    w.beginPath();
    w.moveTo(left,top);
    w.lineTo(left,bottom);
    w.lineTo(right,bottom);
    w.stroke();

    w.fillStyle=T.text;
    w.textAlign="center";
    w.font="14px Arial";

    w.fillText("SINUSOIDAL SIGNALS",300,23);
    w.fillText("Time (seconds)",320,420);

    w.save();
    w.translate(15,205);
    w.rotate(-Math.PI/2);
    w.fillText("Amplitude",0,0);
    w.restore();

    // Draw waveforms
    function plot(color,fn){

        w.beginPath();
        w.strokeStyle=color;
        w.lineWidth=2.5;

        for(let i=0;i<=800;i++){

            const t=start+(end-start)*i/800;

            const xx=X(t);
            const yy=Y(fn(omega*t));

            if(i===0) w.moveTo(xx,yy);
            else w.lineTo(xx,yy);
        }

        w.stroke();
    }

    plot(T.sin,Math.sin);
    plot(T.cos,Math.cos);

    // Moving cursor
    const px=X(time);

    w.strokeStyle=T.radius;
    w.lineWidth=1.8;
    w.setLineDash([5,5]);

    w.beginPath();
    w.moveTo(px,top);
    w.lineTo(px,bottom);
    w.stroke();

    w.setLineDash([]);

    // Moving signal points
    const angle=omega*time;

    function dot(color,value){

        w.fillStyle=color;
        w.beginPath();
        w.arc(px,Y(value),7,0,2*Math.PI);
        w.fill();
    }

    dot(T.sin,Math.sin(angle));
    dot(T.cos,Math.cos(angle));

    // Legend (white background box)
    w.fillStyle=T.legendBg;
    w.fillRect(455,47,115,52);

    w.strokeStyle=T.legendBorder;
    w.lineWidth=1;
    w.strokeRect(455,47,115,52);

    w.textAlign="left";
    w.font="13px Arial";

    w.fillStyle=T.sin;
    w.fillText("● Sine",465,65);

    w.fillStyle=T.cos;
    w.fillText("● Cosine",465,85);
}

// ======================================
// UPDATE DISPLAY
// ======================================

function render(){

    drawCircle();
    drawWaves();

    const f=getFrequency();
    const omega=2*Math.PI*f;

    const angle=(omega*time*180/Math.PI)%360;

    status.textContent=
        "Time: "+time.toFixed(3)+" s | "+
        "Angle: "+angle.toFixed(1)+"° | "+
        "Frequency: "+f.toFixed(2)+" Hz | "+
        "ω: "+omega.toFixed(2)+" rad/s";
}

// ======================================
// ANIMATION
// ======================================

function animate(timestamp){

    if(!playing) return;

    if(lastTimestamp!==null){

        const elapsed=Math.min(
            (timestamp-lastTimestamp)/1000,
            0.05
        );

        time+=elapsed;
    }

    lastTimestamp=timestamp;

    render();

    animationID=requestAnimationFrame(animate);
}

// ======================================
// PAUSE
// ======================================

function pause(){

    playing=false;

    if(animationID!==null){
        cancelAnimationFrame(animationID);
    }

    animationID=null;
    lastTimestamp=null;
}

// ======================================
// PLAY
// ======================================

root.querySelector("#play").addEventListener("click",function(){

    if(playing) return;

    playing=true;
    lastTimestamp=null;

    animationID=requestAnimationFrame(animate);
});

// ======================================
// PAUSE BUTTON
// ======================================

root.querySelector("#pause").addEventListener("click",pause);

// ======================================
// RESET
// ======================================

root.querySelector("#reset").addEventListener("click",function(){

    pause();
    time=0;
    render();
});

// ======================================
// STEP FORWARD
// ======================================

root.querySelector("#forward").addEventListener("click",function(){

    pause();
    time+=getStep();
    render();
});

// ======================================
// STEP BACK
// ======================================

root.querySelector("#back").addEventListener("click",function(){

    pause();
    time=Math.max(0,time-getStep());
    render();
});

// ======================================
// FREQUENCY INPUT
// ======================================

freq.addEventListener("change",function(){

    if(!Number.isFinite(Number(freq.value)) ||
       Number(freq.value)<=0){

        freq.value=1;
    }

    render();
});

// ======================================
// TIME WINDOW INPUT
// ======================================

win.addEventListener("change",function(){

    if(!Number.isFinite(Number(win.value)) ||
       Number(win.value)<=0){

        win.value=2;
    }

    render();
});

// ======================================
// STEP SIZE INPUT
// ======================================

stepInput.addEventListener("change",function(){

    if(!Number.isFinite(Number(stepInput.value)) ||
       Number(stepInput.value)<=0){

        stepInput.value=0.02;
    }
});

// ======================================
// RESPONSIVE RESIZING
// ======================================

let resizeObserver=null;

if(typeof ResizeObserver!=="undefined"){

    resizeObserver=new ResizeObserver(function(){

        render();

    });

    resizeObserver.observe(root.querySelector(".graphs"));
}

window.addEventListener("resize",function(){
    render();
});

// Initial display
render();

})();
</script>

</div>
"""

html = html.replace("ROOT_ID", uid)

# The animation runs entirely in the browser (JavaScript), so play/pause/step
# stay smooth and never trigger Streamlit reruns.
components.html(html, height=1250, scrolling=True)
