const btn = document.querySelector('#btn');
btn.addEventListner('click', (event) => {
	// 전체 화면 전환
    myRequestFullScreen(document.body);
});

function myRequestFullScreen(element) {
	if (element.requestFullscreen) {
    	// 표준 사양
        element.requestFullscreen();
    } else if (element.webkitRequestFullscreen) {
    	// 사파리(safari), 크롬(Chrome)
        element.webkitRequestFullscreen
    } else if (element.mozRequestFullScreen) {
    	// 파이어폭스(Firefox)
        element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
    	// 인터넷 익스플로러 11+ (IE 11+)
        element.msRequestFullscreen();
    }
}

const btnExit = document.querySelector('#btnExit');
btnExit.addEventListener('click', (event) => {
	// 전체 화면 해제
    myCancelFullScreen();
});

function myCancelFullScreen() {
	if (document.exitFullscreen) {
    	// 표준 사양
        document.exitFullscreen();
    } else if (document.webkitCancelFullScreen) {
    	// 사파리(Safari), 크롭(Chrome)
        document.webkitCancelFullScreen();
    } else if (document.mozCancelFullScreen) {
    	// 파이어폭스(Firefox)
        document.mozCancelFullscreen();
    } else if (document.msCancelFullscreen) {
    	// 인터넷 익스플로러 11+ (IE 11+)
        document.msExitFullscreen();
    }
}