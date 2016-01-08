#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions


/* DEFINE VARS */
uint8_t redVal = 0;
uint8_t grnVal = 0;
uint8_t bluVal = 0;

uint8_t prevR = redVal;
uint8_t prevG = grnVal;
uint8_t prevB = bluVal;

int USB;

void changeColor(int *ser, uint8_t redV, uint8_t greenV, uint8_t blueV)
{
    prevR = redVal;
    prevG = grnVal;
    prevB = bluVal;

    uint8_t color[] = {redV, greenV, blueV};
    int r = write( *ser, color, sizeof(color));
    if (r)
    {
        redVal = redV;
        grnVal = greenV;
        bluVal = blueV;
    }
    else
    {
        throw "Failed to write to serial port!";
    }
}


int calculateStep(int prevValue, int endValue)
{
    int step = endValue - prevValue; // What's the overall gap?
    if (step) {                      // If its non-zero,
        step = 1020/step;              //   divide by 1020
    }
    return step;
}


int calculateVal(int step, int val, int i)
{

    if ((step) && i % step == 0) { // If step is non-zero and its time to change a value,
        if (step > 0) {              //   increment the value if step is positive...
            val += 1;
        }
        else if (step < 0) {         //   ...or decrement it if step is negative
            val -= 1;
        }
    }
    // Defensive driving: make sure val stays in the range 0-255
    if (val > 255) {
        val = 255;
    }
    else if (val < 0) {
        val = 0;
    }
    return val;
}

void crossFade(uint8_t R, uint8_t G, uint8_t B, double wait=1000, double hold=0)
{
    int stepR = calculateStep(prevR, R);
    int stepG = calculateStep(prevG, G);
    int stepB = calculateStep(prevB, B);

    for (int i = 0; i <= 1020; i += 1) {
        R = calculateVal(stepR, redVal, i);
        G = calculateVal(stepG, grnVal, i);
        B = calculateVal(stepB, bluVal, i);

        // write color
        try {
            changeColor(&USB, R, G, B);
        } catch (const char* msg) {
            std::cerr << msg << std::endl;
            throw;
        }
        usleep(wait);
    }
    usleep(hold);
}

void Slide(int repeat=1, bool reverse=false, long delay=5000)
{
    uint8_t r, g, b = {0};
    uint8_t R, G, B = {0};
    int counter = 0;

    // write color
    try {
        changeColor(&USB, 0, 0, 0);
    } catch (const char* msg) {
        std::cerr << msg << std::endl;
        throw;
    }

    while ( counter < repeat)
    {
        while(true)
        {
            if ((r < 255) && (!g) && (!b))
            {
                r += 1;
            }
            else if ((r == 255) && (!g))
            {
                g += 1;
                r -= 1;
            }
            else if ((g > 0) && (r > 0))
            {
                g += 1;
                r -= 1;
            }
            else if ((g == 255) && (!b))
            {
                b += 1;
                g -= 1;
            }
            else if ((b > 0) &&  (g > 0))
            {
                b += 1;
                g -= 1;
            }
            else if ((b == 255) && (!r))
            {
                b -= 1;
                r += 1;
                if (repeat) {
                    counter++;
                    break;
                }
            }

            else if ((r < 255) && (b > 0))
            {
                b -= 1;
                r += 1;
            }

            if (!reverse)
            {
                R = r;
                G = g;
                B = b;
            }
            else
            {
                R = b;
                G = g;
                B = r;
            }
            // write color
            try {
                changeColor(&USB, R, G, B);
            } catch (const char* msg) {
                std::cerr << msg << std::endl;
                throw;
            }
            usleep(delay);
        }

        if (repeat > 0)
        {
            counter += 1;
        }
        else {
            ;;
        }

    }
}



void initTest()
{
    int r, g, b= {0};
    int loopTimeout = 2;
    float lightTimeout = 0.25;
    time_t startTime = time(0);
    time_t lastLightTimeout = time(0);
    bool lightState = false;
    while(time(0) - startTime <= loopTimeout)
    {
        if (time(0) - lastLightTimeout == lightTimeout)
        {
            lightState = !lightState;
            lastLightTimeout = time(0);
        }
        if (lightState)
        {
            r = g = b = 255;
        }
        else
        {
            r = g = b = 0;
        }
        // write color
        try {
            changeColor(&USB, r, g, b);
        } catch (const char* msg) {
            std::cerr << msg << std::endl;
            throw;
        }
    }
}

int main()
{
    /* Open File Descriptor */
    USB = open( "/dev/ttyUSB0", O_RDWR| O_NOCTTY );

    /* Error Handling */
    if ( USB < 0 )
    {
        std::cout << "Error " << errno << " opening " << "/dev/ttyUSB0" << ": " << strerror (errno) << std::endl;
        return 1;
    }

    struct termios tty;
    struct termios tty_old;
    memset (&tty, 0, sizeof tty);

    /* Error Handling */
    if (tcgetattr(USB, &tty) != 0)
    {
        std::cout << "Error " << errno << " from tcgetattr: " << strerror(errno) << std::endl;
    }

    /* Save old tty parameters */
    tty_old = tty;

    /* Set Baud Rate */
    cfsetospeed (&tty, (speed_t)B115200);
    cfsetispeed (&tty, (speed_t)B115200);

    /* Setting other Port Stuff */
    tty.c_cflag     &=  ~PARENB;            // Make 8n1
    tty.c_cflag     &=  ~CSTOPB;
    tty.c_cflag     &=  ~CSIZE;
    tty.c_cflag     |=  CS8;

    tty.c_cflag     &=  ~CRTSCTS;           // no flow control
    tty.c_cc[VMIN]   =  1;                  // read doesn't block
    tty.c_cc[VTIME]  =  5;                  // 0.5 seconds read timeout
    tty.c_cflag     |=  CREAD | CLOCAL;     // turn on READ & ignore ctrl lines

    /* Make raw */
    cfmakeraw(&tty);

    /* Flush Port, then applies attributes */
    tcflush( USB, TCIFLUSH );
    if ( tcsetattr ( USB, TCSANOW, &tty ) != 0) {
        std::cout << "Error " << errno << " from tcsetattr" << std::endl;
    }
    sleep(1);

    try {
        while(true)
        {
            //initTest();
            /* *** WRITE *** */
            Slide();
            usleep(100000);
            crossFade(0,255, 0);
            usleep(100000);
            crossFade(255, 20, 50);
            usleep(100000);
        }
    } catch (const char* msg) {
        std::cerr << msg << std::endl;
        close(USB);
        return 1;
    }
}
