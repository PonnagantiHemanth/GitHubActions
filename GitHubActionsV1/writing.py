import tkinter as tk

def update_file():
    additional_items = additional_items_entry.get()
    additional_items_list = additional_items.split(",")

    unique_items = set()

    for item in additional_items_list:
        item = item.strip()
        if item:
            unique_items.add(item)

    with open("testfilter.txt", "w") as file:
        file.write("\n".join(unique_items))

    updated_contents = "\n".join(unique_items)
    text_box.delete("1.0", "end")
    text_box.insert("1.0", updated_contents)


root = tk.Tk()
root.title("Text File Editor")

text_box = tk.Text(root, height=10, width=40)
text_box.pack()

additional_items_label = tk.Label(root, text="Additional Items (comma-separated):")
additional_items_label.pack()

additional_items_entry = tk.Entry(root, width=40)
additional_items_entry.pack()

update_button = tk.Button(root, text="Update File", command=update_file)
update_button.pack()

root.mainloop()
