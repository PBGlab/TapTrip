// ✅ 全域變數統一管理
let map;
let autocomplete;
let locations = [];
let directionsService;
let directionsRenderer;

// ✅ 初始化 Google 地圖
function initMap() {
    console.log("Google Maps API 已載入！✅");

    // **初始化地圖**
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 25.033964, lng: 121.564468 }, // 預設台北101
        zoom: 14
    });

    // **初始化路線服務**
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    // **啟用 Google Maps 自動完成**
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("searchInput"),
        { types: ["establishment"] }
    );

    // **當選擇地點時，加入行程**
    autocomplete.addListener("place_changed", function () {
        let place = autocomplete.getPlace();
        if (!place.geometry) {
            console.log("找不到這個地點!");
            return;
        }
        addLocation(place);
    });
}

// ✅ 初始化拖曳排序
document.addEventListener("DOMContentLoaded", function () {
    new Sortable(document.getElementById("locationList"), {
        animation: 150, // 拖曳動畫時間（毫秒）
        onEnd: function () {
            console.log("🔄 圖卡順序已變更，開始同步 locations 陣列...");

            let newOrder = [];
            document.querySelectorAll(".location-container").forEach((container, index) => {
                let placeName = container.querySelector("strong").innerText;
                let matchedPlace = locations.find(loc => loc.place.name === placeName);
                if (matchedPlace) {
                    matchedPlace.marker.setLabel(String.fromCharCode(65 + index)); // 更新 Marker 標籤
                    newOrder.push(matchedPlace);
                }
            });

            locations = [...newOrder]; // ✅ 更新 locations 陣列
            console.log("📍 更新後的 locations 順序:", locations.map(loc => loc.place.name));

            updateLabels();
            updateRoute();
        }
    });
});

// ✅ 新增地點至清單與地圖
function addLocation(place) {
    if (!place || !place.geometry || !place.geometry.location) {
        console.error("❌ 無效的地點資料：", place);
        return;
    }

    console.log("✅ 新增地點:", place.name);

    const locationList = document.getElementById("locationList");
    let imageUrl = place.photos ? place.photos[0].getUrl({ maxWidth: 100, maxHeight: 100 }) : "https://via.placeholder.com/40";
    let label = String.fromCharCode(65 + locations.length); // A, B, C...

    // ✅ 在地圖上新增標記 (Marker)
    let marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name,
        label: label
    });

    // ✅ 建立圖卡
    let container = document.createElement("div");
    container.classList.add("location-container");

    let markerDiv = document.createElement("div");
    markerDiv.classList.add("location-marker");
    markerDiv.innerHTML = `<span>${label}</span>`; // ✅ 修正 `<span>`

    let card = document.createElement("div");
    card.classList.add("location-card");
    card.innerHTML = `
        <img src="${imageUrl}" alt="${place.name}">
        <div class="location-text">
            <strong>${place.name}</strong><br>
            ${place.formatted_address}
        </div>
    `; // ✅ 修正 `innerHTML`

    let removeBtn = document.createElement("button");
    removeBtn.classList.add("remove-btn");
    removeBtn.innerHTML = "🗑";

    // ✅ 設定刪除按鈕功能
    removeBtn.addEventListener("click", function () {
        container.remove();
        let index = locations.findIndex(loc => loc.place.place_id === place.place_id);
        if (index !== -1) {
            locations[index].marker.setMap(null);
            locations.splice(index, 1);
        }

        updateLabels();
        updateRoute();
    });

    container.append(markerDiv, card, removeBtn);
    locationList.appendChild(container);

    // ✅ 儲存地點與標記
    locations.push({ place, marker });

    updateLabels();
    updateRoute();
}

// ✅ 更新路線
function updateRoute() {
    if (locations.length < 2) {
        directionsRenderer.setDirections({ routes: [] });
        return;
    }

    console.log("🚀 重新規劃路線...");
    console.log("📍 當前地點順序:", locations.map(loc => loc.place.name));

    let waypoints = locations.slice(1, locations.length - 1).map(loc => ({
        location: loc.place.geometry.location,
        stopover: true
    }));

    let request = {
        origin: locations[0].place.geometry.location,
        destination: locations[locations.length - 1].place.geometry.location,
        waypoints: waypoints,
        travelMode: google.maps.TravelMode.DRIVING
    };

    console.log("🛣️ 發送 Google Maps 路線請求:", request);

    directionsService.route(request, function (result, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            console.log("✅ 路線更新成功！");
            directionsRenderer.setDirections(result);

            let totalDuration = result.routes[0].legs.reduce((sum, leg) => sum + leg.duration.value, 0);
            let hours = Math.floor(totalDuration / 3600);
            let minutes = Math.floor((totalDuration % 3600) / 60);
            let durationText = `本路線車程時長總計：${hours} 小時 ${minutes} 分鐘`; // ✅ 修正 `durationText`

            document.getElementById("route-duration").innerText = durationText;
            console.log("⏳ 總車程時間:", durationText);
        } else {
            console.log("❌ 無法獲取路線:", status);
            document.getElementById("route-duration").innerText = "無法計算車程時間";
        }
    });

    updateLabels();
}

// ✅ 更新所有標籤 (A, B, C...)
function updateLabels() {
    document.querySelectorAll(".location-marker span").forEach((markerSpan, index) => {
        let label = String.fromCharCode(65 + index);
        markerSpan.innerText = label;
        if (locations[index]) {
            locations[index].marker.setLabel(label);
        }
    });

    console.log("🏷️ 更新標籤順序:", locations.map(loc => loc.marker.getLabel()));
}
