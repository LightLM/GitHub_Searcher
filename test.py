import tkinter as tk
import requests
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk

url = 'https://api.github.com/search/users?q='


def load_image():
    print(entry.get())
    res = requests.get(url + str(entry.get()) + '&per_page=1')
    print(res.json()['items'][0])
    if res.json()['items']:
        url_image = (res.json()['items'][0]['avatar_url'])
        label.config(text='Loading an image...')
        root.update()
        try:
            response = requests.get(url_image, timeout=10)
        except requests.exceptions.Timeout:
            label.config(text='Timeout error')
        else:
            if response.status_code != 200:
                label.config(text=f'HTTP error {response.status_code}')
            else:
                pil_image = Image.open(BytesIO(response.content))
                image = ImageTk.PhotoImage(pil_image)
                label.config(image=image, text=res.json()['items'][0]['login'], compound='top')


                label.image = image
    else:
        label.config(text='Такого нет(')


if __name__ == '__main__':
    root = tk.Tk()
    entry = ttk.Entry()
    entry.pack()
    tk.Button(root, text='Load an image', command=load_image).pack()
    label = tk.Label(root)
    label.pack()

    root.mainloop()
