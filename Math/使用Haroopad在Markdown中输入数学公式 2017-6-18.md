# 如何用Haroopad在Markdown中写数学公式
##### 准备
在haroopad界面中打开 “文件/偏好设置/Markdown/”然后给“数学表达式选项”中的两个选项打上勾，就可以通过“￥（块状数学公式）￥”或者“￥￥￥（行内数学公式）￥￥￥”来编辑数学公式了（￥需要替换成$），该数学公式应用的是**MathJax**的语法
## 上下标
^上标
_下标
若多于一个字符要用{}括起
例子：
输入：`x^1_2n^{c+2}_c+2`
输出：
$$$x^1_2n^{c+2}_c+2$$$
若是要在左侧或者两侧应用上下标，需要使用\sideset语法
输入：`\sideset{^1_2}{^3_4}x`
输出：
$$$\sideset{^1_2}{^3_4}x$$$
## 括号和分隔符
（）和[]表示其自身，{}是元字符，需要进行转义
输入：`\{\}`
输出：
$$$\{\}$$$
可以通过\left和\right加大括号
输入：`(\frac{x}{y})\left(\frac{x}{y}\right)`
输出：
$$$(\frac{x}{y})\left(\frac{x}{y}\right)$$$
\left和\right必须成对出现，若想使其一边不显示，可以使用.代替原本的符号
输入：`\left.\frac{x}{y}\right|`
输出：
$$$\left.\frac{x}{y}\right|$$$
## 分数
使用\frac{分子}{分母}语法，或者 {分子}\over{分母}
输入：`\frac{n+1}{x+2}或者{{n+1}\over{x+2}}`
输出：
$$$\frac{n+1}{x+2}或者{{n+1}\over{x+2}}$$$
## 开方
\sqrt[根次数]{根号内的内容}
输入：`\sqrt[3]{4}`
输出：
$$$\sqrt[3]{4}$$$
## 省略号
\ldots表示与文本底线对齐的省略号，\cdots表示与文本中线对齐的省略号
输入： `\ldots\cdots`
输出：
$$$\ldots \cdots$$$
## 矢量
输入：`\vec{a} \cdot \vec{b}`
输出：
$$$\vec{a} \cdot \vec{b}$$$
## 积分
输入：`\int_0^1x^2{\rm d}x`
输出：
$$$\int_0^1x^2{\rm d}x$$$
## 极限
输入： `lim_{n\rightarrow+\infty}\frac{1}{n(n+1)}`
输出：
$$$lim_{n\rightarrow+\infty}\frac{1}{n(n+1)}$$$
## 累加，累乘
输入：`累加：\sum_{n=1}^{\infty}a_nx^n累乘：\prod_{n=1}^{\infty}a_nx^n`
输出：
$$$累加：\sum_{n=1}^{\infty}a_nx^n累乘：\prod_{n=1}^{\infty}a_nx^n$$$
## 希腊字母
可以直接用win10自带的中文输入法参照希腊字母一览表里打出来，也可以使用html的语法打出来，用MathJax则是
输入：`\alpha　A　\beta　B　\gamma　\Gamma　\delta　\Delta　\epsilon　E \varepsilon　　\zeta　Z　\eta　H　\theta \epsilon \sigma \rou`
输出：
$$$\alpha　A　\beta　B　\gamma　\Gamma　\delta　\Delta　\epsilon　E \varepsilon　　\zeta　Z　\eta　H　\theta \epsilon \sigma $$$
不过这里我觉得还是win10输入法方便一点
## 数学符号汇总
± ：\pm 
× ：\times 
÷：\div 
∣：\mid

⋅：\cdot 
∘：\circ 
∗: \ast 
⨀：\bigodot 
⨂：\bigotimes 
⨁：\bigoplus 
≤：\leq 
≥：\geq 
≠：\neq 
≈：\approx 
≡：\equiv 
∑：\sum 
∏：\prod 
∐：\coprod

集合运算符： 
∅：\emptyset 
∈：\in 
∉：\notin 
⊂：\subset 
⊃ ：\supset 
⊆ ：\subseteq 
⊇ ：\supseteq 
⋂ ：\bigcap 
⋃ ：\bigcup 
⋁ ：\bigvee 
⋀ ：\bigwedge 
⨄ ：\biguplus 
⨆：\bigsqcup

对数运算符： 
log ：\log 
lg ：\lg 
ln ：\ln

三角运算符： 
⊥：\bot 
∠：\angle 
30∘：30^\circ 
sin ：\sin 
cos ：\cos 
tan ：\tan 
cot ：\cot 
sec ：\sec 
csc ：\csc

微积分运算符： 
y′x：\prime 
∫：\int 
∬ ：\iint 
∭ ：\iiint 
∬∬：\iiiint 
∮ ：\oint 
lim ：\lim 
∞ ：\infty 
∇：\nabla

逻辑运算符： 
∵：\because 
∴ ：\therefore 
∀ ：\forall 
∃ ：\exists 
≠ ：\not= 
≯：\not> 
⊄：\not\subset

戴帽符号： 
y^ ：\hat{y} 
\check{y} ：\check{y} 
y˘ ：\breve{y}

连线符号： 
a+b+c+d¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯：\overline{a+b+c+d} 
a+b+c+d−−−−−−−−−− ：\underline{a+b+c+d} 
a+b+c1.0+d2.0：\overbrace{a+\underbrace{b+c}_{1.0}+d}^{2.0}

箭头符号： 
↑：\uparrow 
↓：\downarrow 
⇑ ：\Uparrow 
⇓：\Downarrow 
→：\rightarrow 
← ：\leftarrow 
⇒ ：\Rightarrow 
⇐ ：\Leftarrow 
⟶ ：\longrightarrow 
⟵ ：\longleftarrow 
⟹：\Longrightarrow 
⟸ ：\Longleftarrow

## 使用指定的字体
{\rm text}如： 
使用罗马字体：text {\rm text} 
其他的字体还有： 
\rm　　罗马体　　　　　　　\it　　意大利体 
\bf　　黑体　　　　　　　　\cal 　花体 
\sl　　倾斜体　　　　　　　\sf　　等线体 
\mit 　数学斜体　　　　　　\tt　　打字机字体 
\sc　　小体大写字母

详细信息可以参考[LikeTech的个人博客](http://blog.csdn.net/lk7688535/article/details/52528307)
