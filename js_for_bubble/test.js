// console.log('hello world')
// alert('hello world')
// document.addEventListener("DOMContentLoaded", function() {
//     console.log('aaa');
// })

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

        // 전체 애니메이션 시간을 15초로 설정
        if (timestamp - animationStartTime <= 15000) {
            // 이전 타임스탬프가 없다면 현재 타임스탬프로 초기화
            if (!lastTimestamp) {
                lastTimestamp = timestamp;
            }

            // 이전 프레임으로부터의 경과 시간 계산
            const elapsedMilliseconds = timestamp - lastTimestamp;
            const elapsedSeconds = elapsedMilliseconds / 1000;

            // 0.5초마다 깜박이도록 설정
            if (elapsedSeconds >= 0.5) {
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
                } else {
                    // 오른쪽에서 왼쪽으로 이동
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