#include "structs.h"

//int word_length = 0;
int word_counter = 0;
int current_amp = 0;
int Pack_cntr = 0;
int Pack_life = 0;
int Bundle_life = 0;

int triangle_divider = 1;
int triangle_multiplier = 1;

int cntr_10uS = 0;
int channel_loop_counter = 1;
int channel_programming_counter = 0;

bool Pause = 0;
bool wave_state_update = true;
bool prefix_status = false;

int current_stack = 1;
int max_stack = 1;

wave_params active_params[17];
USER_T user_input = {"", false, false};
channel_programming_states channel_state;


void setup() {

  Serial.begin(9600);
  
  pinMode(d9, OUTPUT);

  noInterrupts (); // no interrrupts during setup

  //Switch setup code
  
  /* Set MOSI and SCK output, all others input 
  DDRB = (1<<DDB2)|(1<<DDB1)|(1<<DDB0);
  // Enable SPI, Master, set clock rate fck/4 
  SPCR =(1<<SPE)|(1<<MSTR)|(1<<CPOL)|(1<<CPHA)|(1<<SPR1); */
  /* GPIO */
  pinMode(d5, OUTPUT);
  digitalWrite(d5, HIGH); 
  DDRD = (1<<DDD2)|(1<<DDD3)|(1<<DDD6);
  DDRE = (1<<DDE6);
  DDRC = (1<<DDC6);


  //End of Switch Setup code

  //PWM setup code
  //Timer/Counter1 used to controll PWM update
  TCCR1A = (1<<WGM11)|(1<<WGM10);
  TCCR1B = (1<<WGM13)|(1<<WGM12)|(0<<CS12)|(0<<CS11)|(1<<CS10);
  OCR1A = 0xA0;

  TIMSK1 = (1<<TOIE1);

  //Timer/Counter4 used to generate PWM
  DDRC = (1<<DDC7)|(1<<DDC6);
  TCCR4A = (0<<COM4A1)|(1<<COM4A0)|(1<<PWM4A);
  TCCR4B = (1<<PSR4);
  TCCR4B = (0<<DTPS41)|(0<<DTPS40)|(0<<CS43)|(0<<CS42)|(0<<CS41)|(1<<CS40); 
  TCCR4D = (0<<WGM41)|(0<<WGM40);

  //PLL Clock registers (Disabled so code will upload)
  PLLFRQ = _BV(PLLUSB) | _BV(PLLTM1) | _BV(PDIV3) | _BV(PDIV1);
  PLLCSR = _BV(PINDIV) | _BV(PLLE);

 interrupts (); // enable global interrupts
  //Setting 4 bit resolution
  OCR4C = 0x2F;
  //End of PWM setup code

  //default params

  default_stacks ();
  default_variables();
  default_channel_variables ();
  
  
}

ISR (TIMER1_OVF_vect) // Updating PWM on timer4 using timer1 interrupt 
{ 
  //if ( Pause == false)
  //{
    if( current_state != halt)
    {
      word_counter++;
      param_1_wave ();
    }
  //}
  if(channel_state == channel_program)
  {
    cntr_10uS++;
  }  
}

void loop() 
{
  switch (current_state)
  {
    case halt:
      default_variables ();
      break;
    case Play:
    {
     //while( wave_state_update == false)
      //{
        //wait for waveform to finish
      //}
      if (Pack_cntr >= active_params[current_stack].NS)
      {
        //Pause = true;
        word_counter = 0;
        Pack_cntr = 0;
        current_state = Pack_Delay;
        current_amp = 0;
      }
      else if ( prefix_status && (Pack_cntr <= 1))
      {
        current_amp = active_params[current_stack].word_amp/2;
      }
      else
      {
        current_amp = active_params[current_stack].word_amp;
      }

      //Pause = false;

      break;
    }
    case Pack_Delay:
    {
      //Pause = true;
      if (Pack_cntr >= active_params[current_stack].IPD)
      {
        word_counter = 0;
        Pack_cntr = 0;
        Pack_life++;
        if (Pack_life >= active_params[current_stack].NP)
        {
//          Serial.print("Pack_life= \r");
//          Serial.print(Pack_life);
//          Serial.print(" Has reached NP moving to bundle\r");
          Pack_life = 0;
          current_state = Bundle_delay;
        }
        else
        {
          current_state = Play;
       }
      }
      //Pause = false;
      break;
    }
    case Bundle_delay:
    {
      //Pause = true;
      if (Pack_cntr >= active_params[current_stack].IBD)
      {
        word_counter = 0;
        Pack_cntr = 0;
        Bundle_life++;
        if (Bundle_life >= active_params[current_stack].NB)
        {
//          Serial.print("Bundle_life= \r");
//          Serial.print(Bundle_life);
//          Serial.print(" =NB moving to posbundle delay \r");
          Bundle_life = 0;
          current_state = Post_bundle_delay;
        }
        else
        {
          current_state = Play;
       }
      }
      //Pause = false;
      break;
    }
    case Post_bundle_delay:
    {
//      Serial.print("Post bundle finished. going to delay and quit \r");
      //Pause = true;
      //usb_state = IDLE; 
      if ( active_params[current_stack].PBD > 0)
      {
        delay (active_params[current_stack].PBD);
      }
      if (current_stack < max_stack)
      {
        current_stack++;
        word_counter = 0;
        current_amp = active_params[current_stack].word_amp;
        Pack_cntr = 0;
        Pack_life = 0;
        Bundle_life = 0;
        current_state = Play;
      }
      else
      {
        default_variables ();
        max_stack=1;
        current_stack = 1;
        usb_state = IDLE; 
      }      
      //Pause = false;
      break;
    }
    default:
      break;
  }
  triangle_multiplier = (current_amp*2*1.4);
//
//  Serial.print(current_amp);
//  Serial.print("\r");

  switch (usb_state)
  {
    case IDLE:
      getIncomingCMD();
      if(user_input.ready)
      {
        if (user_input.cmd == "*idn?")
        usb_state = IDN;
        else if (user_input.cmd == "reset")
        {
          Serial.print("ACK\r");
          usb_state = RESET;
        }
        else if (user_input.cmd == "stop")
        {
          usb_state = STOP;
        }
        else if (user_input.cmd == "stream")
        {
          usb_state = STREAM;
        }
        else if (user_input.cmd == "update")
        {
          Serial.print("ACK\r");
          usb_state = UPDATE;
        }
        else if (user_input.cmd == "report")
        {
          Serial.print("ACK\r");
          usb_state = REPORT;
        }
        else if (user_input.cmd == "stack")
        {
          usb_state = wave_stack;
        }
        else if (user_input.cmd == "SPW") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = SPW_s;
        }
        else if (user_input.cmd == "shape") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = shape_s;
        }
        else if (user_input.cmd == "IWD") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = IWD_s;
        }
        else if (user_input.cmd == "PePD") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = PePD_s;
        }
        else if (user_input.cmd == "IPD") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = IPD_s;
        }
        else if (user_input.cmd == "IBD") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = IBD_s;
        }
        else if (user_input.cmd == "PBD") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = PBD_s;
        }
        else if (user_input.cmd == "NS") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = NS_s;
        }
        else if (user_input.cmd == "NP") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = NP_s;
        }
        else if (user_input.cmd == "NB") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = NB_s;
        }
        else if (user_input.cmd == "word_amp") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = word_amp_s;
        }        
        else if (user_input.cmd == "CH") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          usb_state = set_channel;
        }
        else if (user_input.cmd == "prefix_on") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          prefix_status = true;
          usb_state = IDLE;
        }
        else if (user_input.cmd == "prefix_off") // SPW\r\n 44\r\n 55\r\n 55\r\n
        {
          prefix_status = false;
          usb_state = IDLE;
        }
        else
        {
          Serial.print("ERR= \r");
          Serial.print(user_input.cmd);
          Serial.print("\r");
          usb_state = ERR;
        }
        user_input = {"", false, false};
      }
      break;
    case ERR:
      usb_state = IDLE;
      Serial.print("error\r");
      for (int n=1; n<=10; n++)
      {
        default_params ( &active_params[n]);
      }        
      default_variables();
      default_channel_variables ();
      break;
    case STOP:
      usb_state = IDLE;
      for (int n=1; n<=10; n++)
      {
        default_params ( &active_params[n]);
      }
      default_variables ();
      default_channel_variables ();
      Serial.print("ACK\r");
      break;
    case IDN:
      Serial.print("Electrotactile_V7\r");
      usb_state = IDLE;
      break;
    case ACK:
      Serial.print("ACK\r");
      usb_state = IDLE;
      break;
    case wave_stack:
      getIncomingCMD();
      if(user_input.ready)
      {
        current_stack = user_input.cmd.toInt();
        if (max_stack <= current_stack)
        {
          max_stack = current_stack;
        }
//        Serial.print("SPW= \r");
//        Serial.print(active_params[current_stack].SPW);
//        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case SPW_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].SPW = user_input.cmd.toInt();
        Serial.print("SPW= \r");
        Serial.print(active_params[current_stack].SPW);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;  
    case IWD_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].IWD = user_input.cmd.toInt();
        Serial.print("IWD= \r");
        Serial.print(active_params[current_stack].IWD);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case PePD_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].PePD = user_input.cmd.toInt();
        Serial.print("PePD= \r");
        Serial.print(active_params[current_stack].PePD);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case IPD_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].IPD = user_input.cmd.toInt();
        Serial.print("IPD= \r");
        Serial.print(active_params[current_stack].IPD);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case IBD_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].IBD = user_input.cmd.toInt();
        Serial.print("IBD= \r");
        Serial.print(active_params[current_stack].IBD);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case PBD_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].PBD = user_input.cmd.toInt();
        Serial.print("PBD= \r");
        Serial.print(active_params[current_stack].PBD);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;      
    case NS_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].NS = user_input.cmd.toInt();
        Serial.print("NS= \r");
        Serial.print(active_params[current_stack].NS);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case NP_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].NP = user_input.cmd.toInt();
        Serial.print("NP= \r");
        Serial.print(active_params[current_stack].NP);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
      case NB_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].NB = user_input.cmd.toInt();
        Serial.print("NB= \r");
        Serial.print(active_params[current_stack].NB);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case word_amp_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].word_amp = user_input.cmd.toInt();
        Serial.print("word_amp= \r");
        Serial.print(active_params[current_stack].word_amp);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case shape_s:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].wave_shape = user_input.cmd.toInt();
        Serial.print("wave_shape= \r");
        Serial.print(active_params[current_stack].wave_shape);
        Serial.print("\r");
        usb_state = IDLE;
        user_input = {"", false, false};
      }
      break;
    case RESET:
      usb_state = IDLE;
      default_stacks ();
      default_variables();
      default_channel_variables ();
      current_stack =1;
      max_stack = 1;
      break;
    case UPDATE:
      usb_state = IDLE;
      for (int n=1; n<= max_stack; n++)
      {
        current_stack = n;
        prepare_params();
      }
      current_stack = 1;
      break;
    case STREAM:
      Serial.print("Streaming\r");
      usb_state = STREAM_IN_PROGRESS;
      default_variables();
      for (int n=1; n<= max_stack; n++)
      {
        current_stack = n;
        prepare_params();
      }
      current_stack =1;
      current_state = Play;
       //active_params[current_stack].SPW = 5;
      break;
      case REPORT:
      usb_state = IDLE;
      switch (current_state)
      {
        case halt:
          Serial.print("halt\r");
          break;
        case Play:
          Serial.print("Play\r");
          break;
        case Pack_Delay:
          Serial.print("Pack_delay\r");
          break;
        case Bundle_delay:
          Serial.print("Bundle_delay\r");
          break;
        default:
          break;
      }
      Serial.print("current stack= \r");
      Serial.print(current_stack);
      Serial.print("\r");
      Serial.print("max stack= \r");
      Serial.print(max_stack);
      Serial.print("\r");
      Serial.print("SPW= \r");
      Serial.print(active_params[current_stack].SPW);
      Serial.print("\r");
      Serial.print("IWD= \r");
      Serial.print(active_params[current_stack].IWD);
      Serial.print("\r");
      Serial.print("PePD= \r");
      Serial.print(active_params[current_stack].PePD);
      Serial.print("\r");
      Serial.print("IPD= \r");
      Serial.print(active_params[current_stack].IPD);
      Serial.print("\r");
      Serial.print("IBD= \r");
      Serial.print(active_params[current_stack].IBD);
      Serial.print("\r");
      Serial.print("PBD= \r");
      Serial.print(active_params[current_stack].PBD);
      Serial.print("\r");
      Serial.print("NS= \r");
      Serial.print(active_params[current_stack].NS);
      Serial.print("\r");
      Serial.print("NP= \r");
      Serial.print(active_params[current_stack].NP);
      Serial.print("\r");
      Serial.print("NB= \r");
      Serial.print(active_params[current_stack].NB);      
      Serial.print("\r");      
      Serial.print("word_amp= \r");
      Serial.print(active_params[current_stack].word_amp);
      Serial.print("\r");
      Serial.print("CH= \r");
      Serial.print(active_params[current_stack].Channel);
      Serial.print("\r");
      break;
    case set_channel:
      getIncomingCMD();
      if(user_input.ready)
      {
        active_params[current_stack].Channel = user_input.cmd.toInt();
        Serial.print("CH= \r");
        Serial.print(active_params[current_stack].Channel);
        Serial.print("\r");
        usb_state = USB_halt;
        channel_state = channel_program;
        user_input = {"", false, false};
      }
      break;
    case STREAM_IN_PROGRESS:
        break;
      case USB_halt:
        break;
    default:
      usb_state = IDLE;
      break;
  }
  if ( channel_state == channel_program)
  {
//     Serial.print("we here bois\r");
//     delay(10);
     if ( cntr_10uS >= 100 ) //has 10us passed?
     {
      cntr_10uS = 0;
      
      if (channel_loop_counter <= 8 )
      {
//        Serial.print("channel_loop_counter\r");
//        Serial.print(channel_loop_counter);
//        Serial.print("\r");
        switch (channel_programming_counter)
        {
          case 0: //put data on PORTE6 or D2
            if ( channel_loop_counter == (9-active_params[current_stack].Channel) ) //this is the channel we want programmed to 1
            {
              PORTE |= (1<<6);
            }
            else //this is not the channel we want programmed to 1
            {
              PORTE &= ~(1<<6);
            }
            PORTD &= ~(1<<6); //make sure clock is low
            channel_programming_counter++;
            break;
          case 1: // set LE to high on PORTD3 or D1
            PORTD |= (1<<3);
            channel_programming_counter++;
            break;
          case 2: //set clock to high to write data
            PORTD |= (1<<6);
            channel_programming_counter++;
            break;
          case 3: //set clock low for next itteration
            PORTD &= ~(1<<6);
            channel_programming_counter=0;
            channel_loop_counter ++;
            break;
          default:
            channel_programming_counter=0;
            break;
        }
//        Serial.print("PORTE\r");
//        Serial.print(PORTE);
//        Serial.print("\rPORTD\r");
//        Serial.print(PORTD);
//        Serial.print("\r");
      }
      else //programming is done, reset everything
      { 
        default_channel_variables ();
        usb_state = IDLE;
      }
    }
  }
}
//
void prepare_params()
{
//  active_params[current_stack].SPW = incomming_params.SPW;
//  active_params[current_stack].IWD = incomming_params.IWD;
//  active_params[current_stack].PePD = incomming_params.PePD;
//  active_params[current_stack].IPD = incomming_params.IPD;
//  active_params[current_stack].IBD = incomming_params.IBD;
//  active_params[current_stack].NS = incomming_params.NS;
//  active_params[current_stack].NP = incomming_params.NP;
//  active_params[current_stack].word_amp = incomming_params.word_amp;
//  active_params[current_stack].Channel = incomming_params.Channel;
//  

      active_params[current_stack].phase[1] = active_params[current_stack].SPW;
      active_params[current_stack].phase[2] = active_params[current_stack].SPW +active_params[current_stack].PePD;
      active_params[current_stack].phase[3] = 2*(active_params[current_stack].SPW)+active_params[current_stack].PePD;
      //active_params[current_stack].phase[4] = 2*(active_params[current_stack].SPW)+active_params[current_stack].PePD+active_params[current_stack].IWD; 
      //active_params[current_stack].phase[4] = 50;
      active_params[current_stack].phase[4] = 2*(active_params[current_stack].SPW)+2*active_params[current_stack].PePD;

}
void default_params (wave_params *params)
{
  params->SPW = 12;// x10us scale pulse-width
  params->IWD = 100;//x10us scale Inter waveform delay
  params->PePD = 12;//x10us scale between pulse delay
  params->IPD = 25;  //Inter-pulse delay
  params->IBD = 25;  //Inter-bundle delay
  params->PBD = 900;  //post-bundle delay
  params->NS = 8; // Number of samples
  params->NP = 4; //number of packages
  params->NB = 4; //number of packages
  params->Channel = 0x01; //what channels are we operating
  params->wave_shape = 1; //number of packages

  params->phase[1] = params->SPW;
  params->phase[2] = params->SPW +params->PePD;
  params->phase[3] = 2*(params->SPW)+params->PePD;
  //params->phase[4] = 100;
  params->phase[4] = 2*(params->SPW)+2*(params->PePD);
  
 
  //voltage parameters
  params->word_amp = 0x0A; // hex number that revolves around a 0x19 ground should be plus/minus 0x17

}


void default_channel_variables ()
{
  channel_state = channel_halt;
  channel_loop_counter = 1;
  PORTE &= ~(1<<6); //Data is low
  PORTD &= ~(1<<6); //make sure clock is low    
  PORTD &= ~(1<<3); //Set LE to low
  PORTD &= ~(1<<2); //Set CLR to always low
  cntr_10uS = 0;
}

void default_variables ()
{
  //word_length = (active_params[current_stack].phase[4]);//Wave cycle total duration
  word_counter = 0;
  current_amp = 0;
  Pack_cntr = 0;
  Pack_life = 0;
  current_state = halt;
  Pause = false;
}

void param_1_wave ()
{
  if(word_counter <= active_params[current_stack].phase[1])
      {
        OCR4A= Ground - current_amp;
        wave_state_update = false;
      }
      else if(word_counter <= active_params[current_stack].phase[2])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[3])
      {
        OCR4A= Ground + current_amp;
      }
      else if(word_counter < active_params[current_stack].phase[4])
      {
        OCR4A= Ground;
        wave_state_update = true;
      }
      else
      {
        //Pause = true;
        word_counter = 0;
        Pack_cntr++;
      }
}

void param_2_wave ()
{
  if(word_counter <= active_params[current_stack].phase[1])
      {
        OCR4A= Ground - current_amp;
      }
      else if(word_counter <= active_params[current_stack].phase[2])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[3])
      {
        if(current_state == Play)
        {
        OCR4A= Ground + 1;
        }
        else
        {
          OCR4A= Ground;
        }
      }
      else if(word_counter <= active_params[current_stack].phase[4])
      {
        OCR4A= Ground;
      }
      else
      {
        Pause = true;
        word_counter = 0;
        Pack_cntr++;
      }
}

void param_3_wave ()
{
  if(word_counter <= active_params[current_stack].phase[1])
      {
        if((word_counter/2)%2 == 0)
        {
          OCR4A= Ground;
        }
        else
        {
        OCR4A= Ground - current_amp;
        }
      }
      else if(word_counter <= active_params[current_stack].phase[2])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[3])
      {
        if(((word_counter-active_params[current_stack].phase[2])/2)%2 == 0)
        {
          OCR4A= Ground;
        }
        else
        {
        OCR4A= Ground + current_amp;
        }
      }
      else if(word_counter <= active_params[current_stack].phase[4])
      {
        OCR4A= Ground;
      }
      else
      {
        Pause = true;
        word_counter = 0;
        Pack_cntr++;
      }
}

void param_4_wave ()
{
  if(word_counter <= active_params[current_stack].phase[1])
      {
        if(word_counter <= active_params[current_stack].phase[1]/2)
        {
          OCR4A= Ground - triangle_multiplier*word_counter/triangle_divider;
        }
        else
        {
          OCR4A= Ground - triangle_multiplier*(active_params[current_stack].phase[1]-word_counter)/triangle_divider;
        }
      }
      else if(word_counter <= active_params[current_stack].phase[2])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[3]-1)
      {
        if(word_counter <= (active_params[current_stack].phase[2]+active_params[current_stack].SPW/2))
        {
        OCR4A= Ground + triangle_multiplier*(word_counter-active_params[current_stack].phase[2])/triangle_divider;
        }
        else
        {
          OCR4A= Ground + triangle_multiplier*(active_params[current_stack].phase[3]-1-word_counter)/triangle_divider;
        }
      }
      else if(word_counter <= active_params[current_stack].phase[4])
      {
        OCR4A= Ground;
      }
      else
      {
        Pause = true;
        word_counter = 0;
        Pack_cntr++;
      }
}

void anodic ()
{
  if(word_counter <= active_params[current_stack].phase[1])
      {
        OCR4A= Ground - current_amp;
      }
      else if(word_counter <= active_params[current_stack].phase[2])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[3])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[4])
      {
        OCR4A= Ground;
      }
      else
      {
        Pause = true;
        word_counter = 0;
        Pack_cntr++;
      }
}

void cathodic ()
{
  if(word_counter <= active_params[current_stack].phase[1])
      {
        OCR4A= Ground + current_amp;
      }
      else if(word_counter <= active_params[current_stack].phase[2])
      {
        OCR4A= Ground;
      }
      else if(word_counter <= active_params[current_stack].phase[3])
      {
        OCR4A= Ground; // + current_amp;
      }
      else if(word_counter <= active_params[current_stack].phase[4])
      {
        OCR4A= Ground;
      }
      else
      {
        Pause = true;
        word_counter = 0;
        Pack_cntr++;
      }
}

void default_stacks ()
{
  default_params ( &active_params[1]);
  default_params ( &active_params[2]);
  default_params ( &active_params[3]);
  default_params ( &active_params[4]);
  default_params ( &active_params[5]);
  default_params ( &active_params[6]);
  default_params ( &active_params[7]);
  default_params ( &active_params[8]);
  default_params ( &active_params[9]);
  default_params ( &active_params[10]);
  current_stack = 1;
  max_stack = 1;
  
}

void getIncomingCMD()
{
  static char incomingByte;
  static int peekByte;
  if (Serial.available() > 0)
  {
    peekByte = Serial.peek();
    if (isAscii(peekByte)) 
    {
      incomingByte = char(Serial.read());
      switch (incomingByte)
      {
        case '\r':
          user_input.CR = true; //would allow cmd like "hi\r\r\r\r\n"
          break;
        case '\n':
          if(user_input.CR)
          {
            user_input.ready = true;
          }
          else
          {
            //Serial.print("LN must be sent after CR ERROR\r");
            usb_state = ERR;
            user_input = {"", false, false};
          }
          break;
        default:
          if(user_input.CR)
          {
            //Serial.print("CR must be followed by LN ERROR\r");
            usb_state = ERR;
            user_input = {"", false, false}; 
          }
          user_input.cmd += incomingByte; //add byte even if \n was missing
          break;
      }
    }
    else
    {
      //ignore the byte for now 
    }
  }
}
