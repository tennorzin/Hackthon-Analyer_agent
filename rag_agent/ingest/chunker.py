def chunk_text(text, max_len=500):
    lines = text.split("\n")
    chunks = []
    curr = ""
    for line in lines:
        if len(curr) + len(line) > max_len:
            chunks.append(curr.strip())
            curr = line
        else:
            curr += " " + line
    if curr:
        chunks.append(curr.strip())
    return chunks