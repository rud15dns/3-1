PImage img;
PImage min;
PImage hour, hour1, hour2, hour3, hour4;
PImage happy_song, christmas_song, refresh_song;
PImage title, title_christmas, title_3; 

float c = 0;
boolean isDayImage = true; 
int fsec, fmin, fhour;
int num = 0;
boolean isMousePressed = false;
int click = 0;
// 시침 색깔. 
float angle1 = 0;
float angle2 = 0;
float angle3 = 0;

PImage day[] = new PImage[2];
import ddf.minim.*;

Minim minim1, minim2, minim3;
AudioPlayer player1, player2, player3;

void setup()
{
  minim1 = new Minim(this);
  minim2 = new Minim(this);
  minim3 = new Minim(this);
  
  player1 = minim1.loadFile("song1.mp3");
  player2 = minim2.loadFile("song2.mp3");
  player3 = minim3.loadFile("song3.mp3");
  
  
  size(432, 432);
  smooth();
  img = loadImage("disk.png");
  img.resize(432, 432);

  
  happy_song = loadImage("happy_song.png");
  christmas_song = loadImage("christmas_song.png");
  refresh_song = loadImage("refresh_song.png");
  
  title = loadImage("title.png");
  title.resize(130, 45);
  title_christmas = loadImage("title_christmas.png");
  title_christmas.resize(200, 50);
  title_3 = loadImage("title_3.png");
  
  day[0] = loadImage("day.png");
  day[0].resize(100, 100);
  day[1] = loadImage("night.png");
  day[1].resize(100, 100);
  
  happy_song.resize(432, 432);
  christmas_song.resize(432, 432);
  refresh_song.resize(432, 432);
  
  hour = loadImage("hour.png");
  hour.resize(432, 432);
  
  hour1 = loadImage("hour1.png");
  hour1.resize(432, 432);
  
  hour2 = loadImage("hour2.png");
  hour2.resize(432, 432);
  
  hour3 = loadImage("hour3.png");
  hour3.resize(432, 432);
  
  hour4= loadImage("hour4.png");
  hour4.resize(432, 432);
}

  
void draw()
{

 background(255);
 
  pushMatrix();
  translate(216, 216);
  scale(1);
  rotate(angle1);
  imageMode(CENTER);
  
  if (click == 0){
  image(img, 0, 0, 432, 432);}
  else if (click == 1){
  image(happy_song, 0, 0, 432, 432);   
  }
  else if (click == 2){
  image(christmas_song, 0, 0, 432, 432);}
  else{
  image(refresh_song, 0, 0, 432, 432);
}
   angle1 += 0.01;
   angle2 = angle1 / 12.0;
  popMatrix();
  
  
  if (click == 0){ if (player3.isPlaying()) {player3.mute();} player1.cue(0);}
  else if (click == 1){
    if (!player1.isPlaying()) {player1.rewind(); player1.play();}
      player1.unmute();
    player1.play();
    player2.cue(0);

  }
  else if (click == 2){
    if (!player2.isPlaying()) {player2.rewind(); player2.play();}
    player1.mute(); player3.cue(0); 
    player2.unmute(); 
    player2.play();

  }
  else{
    if (!player3.isPlaying()) {player3.rewind(); player3.play();}
  player2.mute();
  player3.unmute();
  player3.play();
}



  if (isMousePressed) {
    float angle2R = angle2 % 6.28;
   // println(angle2R);
    if (angle2R < c) {isDayImage = !isDayImage;}
    c = angle2R;
    
    pushMatrix();
    translate(216, 216);
    scale(1);
    rotate(angle2);
    image(hour, 0, 0, 429, 429);
    popMatrix();
     
     
     
    if (isDayImage){
    pushMatrix(); image(day[0], 216 + 6, 216 + 13); popMatrix();}
    else{pushMatrix(); image(day[1], 216 + 6, 217); popMatrix();}
  }
    
    
 
  if (click == 1) {image(title, width/2 + 3, height/2 + 90 + 9);}
  else if (click == 2) {image(title_christmas, width/2 + 5, height/2 + 90 + 11);}
  else if (click == 3) {image(title_3, width/2 + 3, height/2 + 90 + 13);}
  }
void mouseClicked(){//노래에 맞게 색깔이 변함. 
  float distance = dist(mouseX, mouseY, width / 2, height / 2);
  if (distance < 25) { click += 1;
  if (click > 3) click = 0;}
}

void mousePressed() {
  float distance_1 = dist(mouseX, mouseY, width / 2, height / 2);
  if (distance_1 > 230 /4){
  isMousePressed = true;}
}

void mouseReleased() {
  isMousePressed = false;
}

void stop(){
player1.close();
player2.close();
player3.close();
minim1.stop();
minim2.stop();
minim3.stop();
super.stop();}
