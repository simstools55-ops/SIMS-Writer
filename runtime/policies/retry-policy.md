# Retry Policy

一時障害・Schema欠落・出力Component欠落のみ再試行可能です。入力不足、未対応Version、安全上の停止は再試行しません。Alphaでは各Stage最大1回です。
