document.addEventListener("DOMContentLoaded", function () {
    // 取得行程 ID
    const urlParams = new URLSearchParams(window.location.search);
    const itineraryId = urlParams.get("id");

    if (!itineraryId) {
        alert("未找到行程 ID");
        return;
    }

    // 呼叫 Django API 取得行程資訊
    fetch(`/itinerary/${itineraryId}/`)
        .then(response => response.json())
        .then(data => {
            // 顯示行程資訊
            document.getElementById("trip-info").innerText = 
                `行程 ID: ${data.itinerary_id}，開始日期: ${data.start_date}，天數: ${data.days.length}`;

            // 產生行程圖卡
            const container = document.getElementById("trip-container");
            data.days.forEach(day => {
                let card = document.createElement("div");
                card.className = "trip-card";
                card.innerHTML = `
                    <p>第 ${day.day} 天 (${day.date})</p>
                    <p>景點: ${day.attractions.length ? day.attractions.join(", ") : "尚未加入"}</p>
                    <p>住宿: ${day.accommodations.length ? day.accommodations.join(", ") : "尚未加入"}</p>
                    <button onclick="addAttractions(${day.day})">加入景點</button>
                    <button onclick="addHotel(${day.day})">加入住宿</button>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => console.error("載入行程失敗", error));
});

// 加入景點
function addAttractions(day) {
    alert(`前往加入景點: 第 ${day} 天`);
    window.location.href = `/attractions/?day=${day}`;
}

// 加入住宿
function addHotel(day) {
    alert(`前往加入住宿: 第 ${day} 天`);
    window.location.href = `/hotels/?day=${day}`;
}
