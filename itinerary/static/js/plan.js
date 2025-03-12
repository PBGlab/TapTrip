document.getElementById("itinerary-form").addEventListener("submit", function(event) {
    event.preventDefault();  // 防止表單的默認提交行為

    const days = document.getElementById("days").value;
    const startDate = document.getElementById("start_date").value;

    // 使用 fetch 發送 POST 請求
    fetch("/create/", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json", 
            "X-CSRFToken": getCSRFToken()  // 用來處理 CSRF 保護
        },
        body: JSON.stringify({ days: parseInt(days), start_date: startDate })  // 發送 JSON 資料
    })
    .then(response => response.json())  // 解析 JSON 回應
    .then(data => {
        console.log("建立行程 API 回應：", data);  // ✅ 檢查 API 回應
        if (data.error) {
            alert(data.error);  // 顯示錯誤訊息
        } else {
            alert(`行程建立成功！ID：${data.itinerary_id}`);
            window.location.href = `/itinerary/cart/?id=${data.itinerary_id}`;
        }
    })
    .catch(error => {
        console.log('Error:', error);
        alert('發生錯誤，請稍後再試。');
    });
});

// 用來取得 CSRF Token
function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}
