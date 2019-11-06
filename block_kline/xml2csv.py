#encoding=GBK
from bs4 import BeautifulSoup

g_member_code_set = set()

def getMemberSet(block_tag):
    mem_set = set()
    member_tag = block_tag.member
    while member_tag is not None:
        mem_set.add(member_tag.attrs['code'])
        member_tag = member_tag.find_next_sibling('member')

    return mem_set

def getBlockDic(block_tag):
    block_dic = dict()
    while block_tag is not None:
        block_code = block_tag.attrs['blockcode']
        # print(block_code)
        block_dic[block_code] = getMemberSet(block_tag)
        
        block_tag = block_tag.find_next_sibling('block')

    return block_dic

if __name__ == '__main__':
    raw_data = str()
    with open("block.xml", encoding="GBK") as f:
        raw_data = f.read()
    soup = BeautifulSoup(raw_data)
    tag = soup.root.blocks

    f_block  = open("block.csv","w")
    f_membercode = open("membercode.csv","w")

    while tag is not None:
        block_tag = tag.block
        sub_block_tag = block_tag.block

        while block_tag is not None:
            block_member_set = set()
            sub_block_member_list = getBlockDic(sub_block_tag).items()
            for sub_block_member in sub_block_member_list:
                line = str(sub_block_member[0])
                block_member_set |= sub_block_member[1]
                for member in sub_block_member[1]:
                    line += ",{}".format(member)
                f_block.write(line + "\n")

            if sub_block_tag is None:
                block_member_set = getMemberSet(block_tag)

            block_code = block_tag.attrs["blockcode"]
            print(block_code)
            line = str(block_code)
            for block_member in block_member_set:
                line += ",{}".format(block_member)
            f_block.write(line + "\n")

            g_member_code_set |= block_member_set

            block_tag = block_tag.find_next_sibling("block")

        tag = tag.find_next_sibling('blocks')

    member_code_list = list(g_member_code_set)
    for  member_code in member_code_list:
        f_membercode.write(member_code + "\n")
