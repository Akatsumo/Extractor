import requests

url = "https://www.studyiq.net/api/web/searchbycourses?keyword=upsc"


response = requests.get(url)

if response.status_code == 200:
    data = response.json().get("data", [])
    if not data:
        print("No course data found.")
    else:
        print(f"✅ Total Courses Found: {len(data)}\n")
        for course in data:
            print(f"📘 Title       : {course.get('course_title')}")
            print(f"🆔 Course ID   : {course.get('course_id')}")
            print("-" * 60)
else:
    print(f"❌ Failed to fetch data. Status Code: {response.status_code}")




def get_headers():
    url = 'https://backend.studyiq.net/user-auth-ws/v1/auth/generate/admin'
    headers = {
        'api-key': '9A3BDDEEBD4DFB213D3C15D29126151206E47E4F',
        'content-type': 'application/json'
    }
    payload = {
        'platform': 'ADMIN',
        'id': '1013'
    }
    response = requests.post(url, headers=headers, json=payload)
    token = response.json()['token']
    return {"Authorization": f"Bearer {token}"}
    


videos_data = requests.get(f"https://backend.studyiq.net/app-content-ws/v2/course/getDetails?courseId=4368", headers=get_headers())




for item in videos_data.json()["data"]:
    name = item.get("name", "")
    video = item.get("videoUrl")
    pdf = item.get("textUploadUrl")
    if video:
        print(f"{name}: {video}")
    if pdf:
        print(f"{name}: {pdf}")
