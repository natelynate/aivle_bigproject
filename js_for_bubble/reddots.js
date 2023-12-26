// 피험자가 보는 화면 위치와 피험자의 눈동자 위치를 매핑시키기 위해
// 모니터의 특정 영역(중앙, 좌상, 우상, 좌하, 우하)을 5초씩 바라보도록 지시하는 코드

// [더 개선할 사항]
// 현재 점의 좌표 받아오기
// 넘어갈 때 안내 메시지
// 흰색 대신 현재 화면 바탕색으로 쓸 수 없나? (다크 모드 대비 등)
// 처음부터 다시하기 버튼

document.addEventListener("DOMContentLoaded", function() {

    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");

    const radius = 10;
    let isRed = true;
    let lastTimestamp; // 마지막 프레임에서의 타임스탬프
    let animationStartTime; // 애니메이션 시작 시간

    function blinkDot(timestamp) {
        // 애니메이션 시작 시간 초기화
        if (!animationStartTime) {
            animationStartTime = timestamp;
        }

        // 전체 애니메이션 시간을 25초로 설정
        if (timestamp - animationStartTime <= 25000) {
            // 이전 타임스탬프가 없다면 현재 타임스탬프로 초기화
            if (!lastTimestamp) {
                lastTimestamp = timestamp;
            }

            // 이전 프레임으로부터의 경과 시간 계산
            const elapsedMilliseconds = timestamp - lastTimestamp;
            const elapsedSeconds = elapsedMilliseconds / 1000;

            // 0.4초마다 깜박이도록 설정
            if (elapsedSeconds >= 0.4) {
                ctx.clearRect(0, 0, canvas.width, canvas.height); // 캔버스를 지움

                let centerX, centerY;

                // 애니메이션 방향에 따라 중심 좌표 계산
                if (timestamp - animationStartTime <= 5000) {
                    // centerX = canvas.width / 2 - (canvas.width / 2) * (elapsedSeconds / 5);
                    centerX = canvas.width / 2;
                    centerY = canvas.height / 2;
                } else if (timestamp - animationStartTime <= 10000) {
                    centerX = 20;
                    centerY = 20;
                } else if (timestamp - animationStartTime <= 15000) {
                    centerX = 980;
                    centerY = 20;
                } else if (timestamp - animationStartTime <= 20000) {
                    centerX = 20;
                    centerY = 780;
                } else {
                    centerX = 980;
                    centerY = 780;
                }

                if (isRed) {
                    ctx.fillStyle = "red";
                    ctx.strokeStyle = "black"; // 테두리 색 지정 (검은색)
                } else {
                    ctx.fillStyle = "white";
                    ctx.strokeStyle = "red"; // 테두리 색 지정 (빨간색)
                }

                ctx.beginPath();
                ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
                ctx.fill();
                ctx.stroke(); // 테두리 그리기

                isRed = !isRed; // 빨간색과 흰색을 교대로 표시

                // 현재 타임스탬프를 저장
                lastTimestamp = timestamp;
            }

            // 다음 프레임을 예약
            requestAnimationFrame(blinkDot);
        }
    }

    // 초기 호출
    requestAnimationFrame(blinkDot);
    
});




// 윗부분 주석 통째로 해제/적용 핧 것 - 일부 사용 금지

// -----------------------------------------------------



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
