# mysql   notes

## [Numeric Types](https://dev.mysql.com/doc/refman/5.7/en/numeric-types.html)

1、数据类型说明：官方网址 https://dev.mysql.com/doc/refman/5.7/en/integer-types.html

|    Type     | Storage |     Minimum Value      |     Maximum Value      |
| :---------: | :-----: | :--------------------: | :--------------------: |
|             | (Bytes) |   (Signed/Unsigned)    |   (Signed/Unsigned)    |
|  `TINYINT`  |    1    |         `-128`         |         `127`          |
|             |         |          `0`           |         `255`          |
| `SMALLINT`  |    2    |        `-32768`        |        `32767`         |
|             |         |          `0`           |        `65535`         |
| `MEDIUMINT` |    3    |       `-8388608`       |       `8388607`        |
|             |         |          `0`           |       `16777215`       |
|    `INT`    |    4    |     `-2147483648`      |      `2147483647`      |
|             |         |          `0`           |      `4294967295`      |
|  `BIGINT`   |    8    | `-9223372036854775808` | `9223372036854775807`  |
|             |         |          `0`           | `18446744073709551615` |

DECIMAL，声明语法 ：DECIMAL(M,D) 

M是数字的最大数（精度）。其范围为1～65（在较旧的MySQL版本中，允许的范围是1～254），M 的默认值是10; D是小数点右侧数字的数目（标度）。其范围是0～30，但不得超过M。

DECIMAL(M,D)占M+2个字节

FLOAT占四个字节,

DOUBLE占8个字节，

BIGINT，

NUMERIC

## Date and Time Types

DATE

DATETIME

DATESTMAP

## [String Types](https://dev.mysql.com/doc/refman/5.7/en/string-types.html)

CHAR

VARCHAR

BINARY

VARBINARY

BLOB

TEXT

ENUM

SET

## [The JSON Data Type](https://dev.mysql.com/doc/refman/5.7/en/json.html)



