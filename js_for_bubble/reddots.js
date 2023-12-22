document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    const radius = 3;
    let isRed = true;

    function blinkDot() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); // 캔버스를 지움

        if (isRed) {
            ctx.fillStyle = "red";
            ctx.strokeStyle = "gray"
        } else {
            ctx.fillStyle = "white";
            ctx.strokeStyle = "gray"
        }

        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, radius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();

        isRed = !isRed; // 빨간색과 흰색을 교대로 표시
    }

    // 0.5초 간격으로 blinkDot 함수를 호출하여 깜박이게 함
    const intervalId = setInterval(blinkDot, 500);

    // 10초 후에 반복 정지
    setTimeout(function() {
        clearInterval(intervalId);
        console.log("Interval stopped after 10 seconds.");
    }, 10000);
});





// document.addEventListener("DOMContentLoaded", function() {

//     const canvas = document.getElementById("myCanvas");
//     const ctx = canvas.getContext("2d");
//     alert(canvas.clientWidth + ' ' + canvas.clientHeight)

//     // const canvasWidth = canvas.width; // 400
//     // const canvasHeight = canvas.width; // 400
//     const distanceFromRight = 50;
//     const distanceFromBottom = 50;
//     const radius = 5;
//     let isRed = true; // 빨간색과 흰색을 교대로 표시하기 위한 플래그

//     function repeatDot() {
//         ctx.clearRect(0, 0, canvas.width, canvas.height);

//         if (isRed) {
//             ctx.fillStyle = "red";
//         } else {
//             ctx.fillStyle = "white";
//         }

//         ctx.beginPath();
//         ctx.arc(canvas.clientWidth - distanceFromRight,
//                 canvas.clientHeight - distanceFromBottom,
//                 radius, 0, 2 * Math.PI);
//         // ctx.arc(50, 100, 0, 2 * Math.PI);
//         ctx.fill();

//         isRed = !isRed; // 색상을 토글
//     }
//     setInterval(repeatDot, 500);
    

    
    
// ----------------------------


    // requestAnimationFrame(drawRedDot);
    
    // // Get the canvas element
    // const canvas = document.getElementById("myCanvas");
    // const ctx = canvas.getContext("2d");
    
    // alert(canvas.clientWidth + ' ' + canvas.clientHeight)

    // // Set the fill style to red
    // ctx.fillStyle = "red";

    // // Draw a red dot at coordinates (50, 50) with a radius of 5
    // ctx.beginPath();
    // ctx.arc(50, 50, 5, 0, 2*Math.PI);
    // ctx.arc(50, 200, 10, 0, 2*Math.PI);
    // ctx.fill();
// });
