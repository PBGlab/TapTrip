from .models import TripDay, TripDayAttraction, TripLodging

def get_trip_detail_dict(trip):
    trip_days = TripDay.objects.filter(trip=trip).order_by("date")
    total_days = (trip.end_date - trip.start_date).days + 1

    days_data = []
    for day in trip_days:
        attractions = TripDayAttraction.objects.filter(trip_day=day).select_related("attraction").order_by("order")
        attraction_list = []
        for a in attractions:
            attraction_list.append({
                "name": a.attraction.name,
                "city": a.attraction.city.name,
                "link": a.attraction.link,
                "image_url": a.attraction.image_url,
                "googlemap": a.attraction.googlemap,
                "hashtag": a.attraction.hashtag,
                "order": a.order,
            })

        days_data.append({
            "id": day.id,
            "date": day.date,
            "attraction_count": len(attraction_list),
            "attractions": attraction_list,
        })

    # 取得住宿資料
    trip_lodgings = TripLodging.objects.filter(trip=trip).select_related("lodging")
    lodging_data = []
    for link in trip_lodgings:
        l = link.lodging
        lodging_data.append({
            "id": l.id,
            "name": l.name,
            "address": l.address,
            "checkin": l.check_in,
            "checkout": l.check_out,
            "price": l.price,
            "link": l.link,
            "image": l.image,
        })

    return {
        "trip": trip,
        "total_days": total_days,
        "days": days_data,
        "has_lodging": bool(lodging_data),
        "lodgings": lodging_data,
    }
