##
# Author: Tung Thanh Le 
# ttungl@gmail.com
##

class Extract_Network:

    def __init__(self, path):
        self.res = []
        self.path = path
        self.stats_file = self.path + 'm5out/stats.txt'
        
    def parse_features(self, feat_list=[]):
        if not feat_list: return -1
        
        fp = open(self.stats_file, 'r')
        lines = fp.readlines()
        for i in lines:
            for j in feat_list:
                if j in i:
                    if j == 'sim_seconds':
                        v1, _ = i.split("#")
                        _, v2 = v1.split(j)
                        v = v2.replace(" ","")
                    else:
                        _, v = i.split(j)

                    v = v.lstrip().rstrip().replace("|","")
                    if "::" in j:
                        self.res.append(j.split("::")[0].strip() + " = " + str(v))
                    else:
                        self.res.append(j +" = "+ str(v))
                    # print(j + " = " + str(v))

    def write_to_file(self):
        with open(self.path + 'interconnect-routing-gym/network_stats.txt', 'w') as filehandle:
            for listitem in self.res:
                filehandle.write('%s\n' % listitem)
        print self.res
        self.res = []