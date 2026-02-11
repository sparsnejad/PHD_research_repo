%[time,amp] = plotter_2(BF, BDC, TF, TDC, length)

   test= zeros(1,1000);
   for i= 1:1000
       test(1,i)= -1*(1001-i)/100000;;
   end

   subplot(4,1,1);
   [time1,amp1] =plotter_2(1, 100, 10, 3, 500);
   time1= cat(2, test, time1);
   amp1= cat(2, zeros(1,1000), amp1);
   %amp1(1,1:4000)= 0;
   plot(time1,amp1)   
   title('10Hz low intensity tapping')
   subplot(4,1,2);
   [time2,amp2] =plotter_2(1, 100, 200, 10, 500);
   time2= cat(2, test, time2);
   amp2= cat(2, zeros(1,1000), amp2);
   plot(time2,amp2)
   title('100Hz low intensity vibration')
   subplot(4,1,3);
   [time3,amp3] =plotter_2(1, 100, 1, 0.1, 500);
   time3= cat(2, test, time3);
   amp3= cat(2, zeros(1,1000), amp3);
   %amp3(1,1:4000)= 0;
   plot(time3,amp3)
   title('10Hz high intensity tapping')
   subplot(4,1,4);
   [time4,amp4] =plotter_2(1, 100, 32, 10, 500);
   time4= cat(2, test, time4);
   amp4= cat(2, zeros(1,1000), amp4);
   plot(time4,amp4)
   title('100Hz high intensity vibration')
   


