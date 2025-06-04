def generate_captions(topic):
    if not topic:
        topic = "random fun"
    return [
        f"When you're into {topic} but life has other plans...",
        f"{topic.title()} mode: ON 🔥",
        f"This is what {topic} looks like on Mondays 😩"
    ]
