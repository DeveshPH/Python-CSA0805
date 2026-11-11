def normalise_name(name):
    return " ".join(name.casefold().split())

def normalise_phone(phone):
    return "".join(ch for ch in phone if ch.isdigit())

def merge_contacts(*sources):
    merged = {}
    for source in sources:
        for contact in source:
            key = (normalise_name(contact["name"]), normalise_phone(contact["phone"]))
            if key not in merged:
                merged[key] = dict(contact)
            else:
                for field, value in contact.items():
                    if value and not merged[key].get(field):
                        merged[key][field] = value
    return list(merged.values())

if __name__ == "__main__":
    a = [{"name":"Anu S","phone":"+91 98765 43210","email":""}]
    b = [{"name":" anu s ","phone":"919876543210","email":"anu@example.com"}]
    print(merge_contacts(a,b))
