# 疫情数据可视化

**直接运行main.py即可，时间稍长，请耐心等待**
***

## 文件介绍
- Data.zip
    - 为项目原始为解压处理的数据压缩包
- Data
    - 解压得到的数据文件夹
- 实践概述.md
    - 实践概述
- main.py
    - 主程序，即生成并渲染数据可视化图片的程序
- README.md
    - 项目说明文档
- requirements.txt
    - 依赖环境
- unzip.py
    - 用于解压压缩包的文件
- 2021年新冠累计确诊数据地图.html
    - 为网页的html源文件，可以通过浏览器预览

## 思路介绍

### 解压处理文件
- 源码展示
```python
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
```
1. 通过zipfile解压文件夹
2. 通过pandas库导出Series类型的数据
3. 利用字典存储2021年全国城市累计确诊数据，利用字典的get函数避免重复存储
4. 将数据导出为列表格式，并且**剔除所有累计确诊为0的数据**
5. 写入文件data.txt，避免运行主程序时运行该程序遍历csv文件。可通过读取data.txt直接读取Data.zip压缩包中的数据

### 生成可视化疫情数据
- 源码展示
```python
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
```
1. 利用pyecharts的Geo类型生成地图并渲染
2. 根据已有数据，划分数据分段范围
3. 读入文件data.txt，并导入为列表类型，转换为pyecharts可处理的数据格式
4. 渲染，生成本地html文件"2021年新冠累计确诊数据地图.html"
5. 通过默认本地浏览器打开html文件