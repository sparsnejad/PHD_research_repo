//enum operation_states { Idle, Play, Pack_Delay, Bundle_delay };

typedef struct
{
  // time-based commands x10us scale
  int SPW;// x10us scale pulse-width
  int IWD;//x10us scale Inter waveform delay
  int PePD;//x10us scale between pulse delay
  //uint8_t  Class; //indirect time-based characters extracted from the times based ones
  int IPD;  //Inter-pulse delay
  int IBD;  //Inter-bundle delay
  int PBD; //post-bundle-delay
  int NS; // Number of samples
  int NP; //number of packages
  int NB; //number of packages
  
  //voltage parameters
  int word_amp; // hex number that revolves around a 0x19 ground should be plus/minus 0x17
  int phase[4];
  int Channel;
  int wave_shape;

} wave_params;

typedef struct {
  String cmd;
  bool ready;
  bool CR; 
} USER_T;

/* State Machine  */
enum USB_t {
  IDLE,
  IDN,
  ERR,
  ACK,
  RESET,
  STOP,
  STREAM,
  REPORT,
  UPDATE,
  SPW_s,
  IWD_s,
  PePD_s,
  IPD_s,
  IBD_s,
  PBD_s,
  NS_s,
  NP_s,
  NB_s,
  shape_s,
  word_amp_s,
  set_channel,
  STREAM_IN_PROGRESS,
  USB_halt,
  wave_stack
};

enum operation_states { Play, halt, Pack_Delay, Bundle_delay, Post_bundle_delay};
enum channel_programming_states { channel_halt, channel_program };
enum operation_states current_state = halt;
enum USB_t usb_state = IDLE;

void getIncomingCMD();
void param_1_wave ();
void param_2_wave ();
void param_3_wave ();
void param_4_wave ();
void anodic ();
void cathodic ();
void copy_params();
void default_params (wave_params *params);
void default_variables ();
void default_stacks ();
void default_channel_variables ();



#define d5 5
#define d9 9
#define Ground 0x19
