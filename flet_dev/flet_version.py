import flet as ft
import requests

url = 'https://api.github.com/search/users?q='


def main(page: ft.Page):
    def textbox_changed(e):
        t.value = e.control.value
        t.update()

    def button_clicked(e):
        nickname = str(tb.value)
        res = requests.get(url + str(nickname) + '&per_page=1')
        if res.status_code == 200 and res.json()['items'] != [] and str(
                res.json()['items'][0]['login']).lower() == nickname.lower():
            info = res.json()['items'][0]
            url_image = (res.json()['items'][0]['avatar_url'])
            con.image_src = url_image
            con.content = ft.Text(value=f'Никнейм: {info["login"]}',
                                  color=ft.colors.YELLOW
                                  )
            con.url = info['html_url']
            dd.options = [ft.dropdown.Option(f'{i["name"]}') for i in requests.get(info['repos_url']).json()[:5]]
            dd.hint_text = f'{len(requests.get(info["repos_url"]).json()[:5])} реп профиля под именем: {info["login"]}'
        else:
            con.image_src = 'svadebnym_spetsialistam_kak_ispolzovat_vkontakte_dlya_prodvizheniya_biznesa.jpg'
            con.content = ft.Text(value=f'Такого профиля нет',
                                  color=ft.colors.YELLOW
                                  )
            con.url = ''
        dd.update()
        con.update()
        print(res.text)

    con = ft.Container(
        content=ft.Text('Начнем поиск'),
        width=300,
        height=300,
        padding=ft.padding.only(bottom=5),
        image_src='svadebnym_spetsialistam_kak_ispolzovat_vkontakte_dlya_prodvizheniya_biznesa.jpg',
        alignment=ft.alignment.bottom_center

    )
    b = ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=button_clicked, data=0
    )
    t = ft.Text(
        width=300
    )
    tb = ft.TextField(
        label='Введи никнейм, который хочешь найти:',
        on_change=textbox_changed,
        width=300,
    )
    page.add(ft.Row(
        controls=[tb, b]
    ))
    page.add(ft.Column(
        controls=[t, con]
    ))

    def dropdown_changed(e):
        t_dd.value = f"Ссылка на репу: https://github.com/{con.content.value.split()[-1]}/{dd.value}"

        page.update()

    t_dd = ft.Text()
    dd = ft.Dropdown(
        on_change=dropdown_changed,
        hint_text='Сначала найди по никнейму',
        options=[
            ft.dropdown.Option("Пока ничего нет")
        ],
        width=300,
    )
    page.add(dd, t_dd)


if __name__ == '__main__':
    ft.app(target=main)
