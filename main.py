# 主程序 位于main.py文件 第36行

from pyecharts import options as opts
from pyecharts.charts import Geo
import os
import webbrowser
from zipfile import ZipFile
import pandas


def unzip() -> list:
    """解压Data.zip并将导出为pyecharts可处理的格式

    Returns:
        list: which contains the data of Covid-19
    """
    with ZipFile('Data.zip', 'r') as myzip:
        myzip.extractall('Data')
        namelist = myzip.namelist()
    data_zip = {}
    for item in namelist:
        data = pandas.read_csv('Data\\'+item, sep=',',
                               header='infer', usecols=[0, 1])
        temp_dict = data['城市'].to_dict()
        temp_val = data['新增确诊'].to_dict()
        for item in temp_dict.keys():
            data_zip[temp_dict[item]] = data_zip.get(
                temp_dict[item], 0) + temp_val[item]
    data = []
    for key, value in data_zip.items():
        if value != 0:
            data.append((key, value))
    return data


def main():
    """main
    """
    data = unzip()

    def visual_map() -> Geo:
        c = (
            Geo(init_opts=opts.InitOpts(bg_color='#eee'))
            .add_schema(maptype="china")
            .add("累计确诊", data)
            .set_global_opts()
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=[
                    {"min": 5000, "label": '>5000', "color": "#801C1B"},
                    {"min": 1000, "max": 5000,
                        "label": '1000-5000', "color": "#FF3030"},
                    {"min": 100, "max": 999, "label": '100-999', "color": "#FF4500"},
                    {"min": 50, "max": 99, "label": '50-99', "color": "#FF7F50"},
                    {"min": 10, "max": 49, "label": '10-49', "color": "#FFA500"},
                    {"min": 1, "max": 9, "label": '1-9', "color": "#FFDEAD"},
                    {"max": 0, "label": '0', "color": "green"}
                ]),
                title_opts=opts.TitleOpts(title="2021年新冠累计确诊数据地图"),
            )
            .render("2021年新冠累计确诊数据地图.html")
        )
        return c

    visual_map()
    path = os.path.abspath("2021年新冠累计确诊数据地图.html")
    webbrowser.open_new_tab(path)


if __name__ == '__main__':
    main()
