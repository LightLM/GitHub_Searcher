import flet as ft
import requests
import json

url = 'https://api.github.com/search/users?q='


def main(page: ft.Page):
    def textbox_changed(e):
        v = e.control.value
        t.value = v
        dict_a[action].append(v)
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
            reps_nick = requests.get(info['repos_url']).json()[:5]
            dd.options = [ft.dropdown.Option(f'{i["name"]}') for i in reps_nick]
            dd.hint_text = f'{len(requests.get(info["repos_url"]).json()[:5])} реп профиля под именем: {info["login"]}'
            if not info["login"] in a:
                a[info["login"]] = {'avatar_url': info['avatar_url'], 'reps': reps_nick, 'html_url': info['html_url']}
                with open("data.json", "w") as refresh:
                    json.dump(a, refresh)
                with open("actions.json", "w") as refresh_actions:
                    json.dump(dict_a, refresh_actions)
                dd_2.options = [ft.dropdown.Option(i) for i in a]
        else:
            con.image_src = 'svadebnym_spetsialistam_kak_ispolzovat_vkontakte_dlya_prodvizheniya_biznesa.jpg'
            con.content = ft.Text(value=f'Такого профиля нет',
                                  color=ft.colors.YELLOW
                                  )
            con.url = ''
        page.update()

    def dropdown_changed(e):
        t_dd.value = f"Ссылка на репу: https://github.com/{con.content.value.split()[-1]}/{dd.value}"
        page.update()

    def button_clicked_upload(e):
        name = dd_2.value
        con.image_src = a[name]['avatar_url']
        con.url = a[name]['html_url']
        con.content = ft.Text(value=f'Никнейм: {name}',
                              color=ft.colors.YELLOW
                              )
        dd.options = [ft.dropdown.Option(f'{i["name"]}') for i in a[name]['reps']]
        dd.hint_text = f'{len(a[name]["reps"])} реп профиля под именем: {name}'
        page.update()

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
    bt = ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=button_clicked_upload, data=0
    )
    t = ft.Text(
        width=300
    )
    t_dd = ft.Text()
    tb = ft.TextField(
        label='Введи никнейм, который хочешь найти:',
        on_change=textbox_changed,
        width=300,
    )

    dd = ft.Dropdown(
        on_change=dropdown_changed,
        hint_text='Сначала найди по никнейму',
        options=[
            ft.dropdown.Option("Пока ничего нет")
        ],
        width=300,
    )

    dd_2 = ft.Dropdown(
        hint_text='Загрузка профиля (по нику)',
        options=[
            ft.dropdown.Option(i) for i in a
        ],
        width=300,
    )

    page.add(ft.Row(
        controls=[tb, b]
    ))
    page.add(ft.Column(
        controls=[t, con]
    ))
    page.add(dd, t_dd)
    page.add(ft.Row([dd_2, bt]))


if __name__ == '__main__':
    with open("data.json", "r") as fh:
        a = json.load(fh)
    with open("actions.json", "r") as dict_actions:
        dict_a = json.load(dict_actions)
    for i in dict_a:
        print(i)
        print(dict_a[i])
    action = str(int(list(dict(dict_a).keys())[-1]) + 1)
    dict_a[action] = []
    ft.app(target=main)
