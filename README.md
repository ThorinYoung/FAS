# FAS(Face Animation System)![img](D:\notes\pic\05CFA71C-1715681506062.png)

#### It may take a while to load all images.

### Quick start![img](./example/pngs/05CE8C75.png)

1. cuda 10.x is recommended, while cuda 11.x / 12.x have not been tested for stylegan2

2. refer to env.yaml to create the environment or use this command below:

   ```conda env create -n fas -f env.yaml```
   
   if any problem occurred, please install specific packages manually, then run

   ```conda activate fas```

3. get checkpoints:
   https://pan.quark.cn/s/350c14d48e34

   put them all in ./checkpoints

4. run the main.py 

   ```python main.py```

   you can get the main window as below:

 <img src="./example/1.png" alt="Description of your image">

### Example![img](./example/pngs/05CEBAF7.png)

Here are some examples: 

<p align="center">
  <img src="./res/res/0.gif" width="256" />
  <img src="./res/res/2.gif" width="256" />
  <img src="./res/res/3.gif" width="256" />
</p>

<p style="text-align: center;" align='center'>
  <span style="display: inline-block; width: 256px;" width='256'>source ||</span>
  <span style="display: inline-block; width: 256px;" width='256'>result1 ||</span>
  <span style="display: inline-block; width: 256px;" width='256'>+smile</span>
</p>

<p align="center">
  <img src="./res/res/4.gif" width="256" />
  <img src="./res/res/5.gif" width="256" />
  <img src="./res/res/6.gif" width="256" />
</p>

<p style="text-align: center;" align='center'>
  <span style="display: inline-block; width: 256px;" width='256'>result2 ||</span>
  <span style="display: inline-block; width: 256px;" width='256'>-age ||</span>
  <span style="display: inline-block; width: 256px;" width='256'>+age +glass</span>
</p>

Examples with UI:



<p align='center'>
    <p align='left' style="font-size: 20px;"><span>To generate different faces:</span></p>
    <p align='center'><img src="./example/1.gif" width='800' /></p>
    <p align='left' style="font-size: 20px;"><span>To adjust face attributes:</span></p>
	<p align='center'><img src="./example/2.gif" width='800' /></p>
    <p align='left' style="font-size: 20px;"><span>To generate face videos:</span></p>
    <p align='center'><img src="./example/3.gif" width='800' /></p>
</p>

### Contributor![img](./example/pngs/05CFA71C.png)

Gratitude to Senior Song Jiapeng for his invaluable assistance! 

Acknowledgments to the contributors of https://github.com/a312863063/generators-with-stylegan2 

Special thanks to the contributors of https://github.com/AliaksandrSiarohin/first-order-model

### License

The project is licensed under the [Apache License 2.0] - Please refer to the [LICENSE] file for detailed information.