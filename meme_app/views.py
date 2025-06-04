from django.shortcuts import render
from .caption_suggester import get_captions_for_topic
from .image_captioner import create_meme
import os
from django.conf import settings

def meme_home(request):
    if request.method == "POST":
        if "topic" in request.POST and "image" in request.FILES:
            topic = request.POST["topic"]
            captions = get_captions_for_topic(topic)
            image = request.FILES["image"]
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(image_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            memes = []
            for idx, caption in enumerate(captions):
                meme_filename = f"meme_{idx}_{image.name}"
                meme_path = os.path.join(settings.MEDIA_ROOT, meme_filename)
                create_meme(image_path, caption, meme_path)
                meme_url = os.path.join(settings.MEDIA_URL, meme_filename)
                absolute_url = request.build_absolute_uri(meme_url)
                memes.append({
                    "caption": caption,
                    "meme_url": meme_url,
                    "absolute_url": absolute_url,
                })
            return render(request, "result.html", {
                "memes": memes,
                "topic": topic,
            })
        elif "caption" in request.POST and "image_name" in request.POST:
            caption = request.POST["caption"]
            topic = request.POST.get("topic", "")
            image_name = request.POST["image_name"]
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            output_path = os.path.join(settings.MEDIA_ROOT, "generated_meme.jpg")
            create_meme(image_path, caption, output_path)
            meme_url = os.path.join(settings.MEDIA_URL, "generated_meme.jpg")
            absolute_url = request.build_absolute_uri(meme_url)
            return render(request, "result.html", {
                "meme_url": meme_url,
                "caption": caption,
                "topic": topic,
                "absolute_url": absolute_url,
            })
    return render(request, "index.html")
