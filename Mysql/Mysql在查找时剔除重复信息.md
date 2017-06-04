#MySQL 查询不重复信息
由于爬虫设计的不成熟，经常断线然后停止工作，为了偷懒也没有加能够让爬虫保存当前工作进度的功能，所以总是需要手动修改爬虫开始爬取的阶段，这样也就不可避免的会产生一些重复的数据，当然，id是不会重复的，但是名字，点击数这些东西，就不一样了。

于是，上网搜索，找到一条可以直接查询在某一字段不重复的信息的语句
`select *,count(distinct repeatColumn) from table group by reapeatColumn`
`select * from table`是最常用的查询数据库表内信息的语句，而count（）函数，能够对于某一类信息进行计数，distinct reapeatColumn用distinct来标记要查找的是否重复的字段，group by将找到剔除重复字段的信息设为一个分组，然后用这个语句就可在查找时剔除掉其它在repeatColumn上有重复的信息了。