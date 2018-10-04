# this will be pasted on line 193 of reduce2.py
f = open("../../data.txt", "r")
f.readline()
f.readline()
D_A_Mpc = f.readline().strip()
f.close()

D_A_kpc = D_A_Mpc*1000.0

pi = 3.141592653589793

pixel_scale = (15*180*3600/pi)*(1/0.984)/D_A_kpc

scale = pixel_scale

string = str(scale)


# this edit will replace line 196
os.system("csmooth threshed_broad.fits clobber=yes outfile=smoothed.fits sclmap=\"\" sclmin=" + string + " sclmax=" + string + " sclmode=compute outsigfile=. outsclfile=. conmeth=fft conkerneltype=gauss sigmin=4 sigmax=5")