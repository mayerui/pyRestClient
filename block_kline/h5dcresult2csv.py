#encoding=GBK

class CandleItem:
    code =0
    time = 0
    open_px = 0
    high_px = 0
    low_px = 0
    close_px = 0
    vol = 0
    money = 0
    reserve = 0
    def __init__(self, code, line):
        self.code = code
        cols = line.strip().split("(")
        self.time  = str(cols[1][0:cols[1].find(")")])
        self.open_px  = str(cols[2][0:cols[2].find(")")])
        self.high_px  = str(cols[3][0:cols[3].find(")")])
        self.low_px  = str(cols[4][0:cols[4].find(")")])
        self.close_px  = str(cols[5][0:cols[5].find(")")])
        self.vol  = cols[6][0:cols[6].find(")")]
        self.money  = str(float(cols[7][0:cols[7].find(")")]))
        self.reserve = str(float(cols[8][0:cols[8].find(")")]))
        
    def __str__(self):
        return self.code +"," + self.time + "," +self.open_px + "," +self.high_px + "," +self.low_px + "," +self.close_px + "," +self.vol + "," +self.money + ",,,,,\n"


if __name__ == '__main__':
    code  =str()
    workspace = "D:/需求/32国金板块K线修复20191031/"
    with open(workspace + "h5dc_result.out", "r") as f_in, \
            open(workspace + "h5dc_result.csv","w") as f_out:
        lines = f_in.readlines()
        for line in lines:
            if "code" in line:
                code = line[len("code("):len("code(") + 6]
                continue
            elif "candle_item" in line:
                kline = CandleItem(code, line)
                f_out.write(str(kline))
