import java.text.SimpleDateFormat;
import java.text.FieldPosition;
import java.util.Date;
import java.util.TimeZone;
class CoverageIDLabel{
    private String coverageIDLabel;
    public CoverageIDLabel (String coverageIDLabel){
        this.coverageIDLabel=coverageIDLabel;
    }public void affiche(){
        System.out.println("je suis le coverageIDLabel : "+ this.coverageIDLabel);
    }
    public String getCoverageIDLabel(){
        return this.coverageIDLabel;
    }
    public String getStringDate(){
        int index=this.coverageIDLabel.indexOf("___");
        String rep=this.coverageIDLabel.substring(index+3,index+23);
        rep=rep.replace(".",":");
        return rep;
    }
    public Date getDate() throws Exception {  // date en UTC
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
        Date rep = sdf.parse(this.getStringDate());
        return rep;
    }
    public long getTSInMiliDate() throws Exception {
        return (this.getDate().getTime());
    }
    public String getDateDeLaPrevision (long echeanceSecondes) throws Exception {  // calcul la date de prevision mise au format "yyyy-MM-dd'T'HH:mm:ss'Z'" 
        long TSPrevision=this.getTSInMiliDate()+echeanceSecondes*1000;
        Date datePrevision=new Date(TSPrevision);
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
        StringBuffer strb =new StringBuffer();
        sdf.format(datePrevision,strb,new FieldPosition(0));
        return (strb.toString());
    }
    public double getAge() throws Exception {  // calcul l'age en heure
       long now=new Date().getTime(); // l'heure locale du serveur
       // il faut la transformer en UTC :
       int decal=TimeZone.getDefault().getOffset(now);  // calcul du décalage par rapport à UTC
       now=now-decal; // calcul de l'heure actuelle UTC
       double age=(now-this.getTSInMiliDate())/1000./3600.;
       return (age);
    }
    public boolean isFutur() throws Exception {
        if (this.getAge() <= 0) {
            return true;
        }
        else {
            return false;
        }
    }
    public String getName(){
        int index=this.coverageIDLabel.indexOf("___");
        return (this.coverageIDLabel.substring(0,index));
    }
    public String getSuffixe(){
        int index=this.coverageIDLabel.indexOf("___");
        return (this.coverageIDLabel.substring(index+23,this.coverageIDLabel.length()));
    }
    public boolean isCumul(){
        int index=this.coverageIDLabel.indexOf("Z_P");
        if (index<0) return false;
        return true;
    }
    public String getCumul(){
        int index=this.coverageIDLabel.indexOf("Z_P");
        if (index<0) return null;
        return (this.coverageIDLabel.substring(index+3,this.coverageIDLabel.length()));
    }
    public boolean aIgnorer(){  // sélectionne les coverageIDLabel à ignorer
        String label=this.coverageIDLabel;
        //System.out.println("isCumul: "+this.isCumul());
        //System.out.println("cumul: "+this.getCumul());

        if (this.isCumul()){    // cas des cumuls
            //System.out.println("on teste cumul sur 1 heure");
            if (this.getCumul().equals(new String("T1H"))) { // on traite les cumuls sur 1 heure 
                //System.out.println("on traite les cumuls sur 1 heure");
                return false;
            }
            else {
                return true;   // tous les autres cumuls seront ignorés
            }
        }
        if (label.contains("TURBULENT_KINETIC_ENERGY")) return true;
        if (label.contains("GEOMETRIC_HEIGHT__")) return true;
        if (label.contains("SPECIFIC_CLOUD_ICE_WATER")) return true;
        if (label.contains("SPECIFIC_RAIN_WATER_CONTENT__ISOBARIC_SURFACE")) return true; 
        if (label.contains("SPECIFIC_RAIN_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL")) return true;
        if (label.contains("SPECIFIC_SNOW_WATER_CONTENT__")) return true;
        if (label.contains("SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE")) return true;
        if (label.contains("RELATIVE_HUMIDITY__ISOBARIC_SURFACE___")) return true;
        if (label.contains("LOW_CLOUD_COVER__GROUND")) return true;
        if (label.contains("HIGH_CLOUD_COVER__GROUND")) return true;
        if (label.contains("MEDIUM_CLOUD_COVER__GROUND")) return true;
        if (label.contains("CONVECTIVE_CLOUD_COVER__GROUND")) return true;
        if (label.contains("PRESSURE__SPECIFIC_HEIGHT_LEVEL_")) return true;
        if (label.contains("PRESSURE__GROUND_OR_WATER")) return true;
        if (label.contains("TOTAL_PRECIPITATION_RATE__SPECIFIC_HEIGHT")) return true;
        if (label.contains("TOTAL_PRECIPITATION_RATE__ISOBARIC")) return true;
        if (label.contains("ABSOLUTE_VORTICITY__ISOBARIC")) return true;
        if (label.contains("TURBULENT_KINETIC_ENERGY__SPECIFIC_HEIGHT")) return true;
        if (label.contains("TURBULENT_KINETIC_ENERGY__ISOBARIC")) return true;
        if (label.contains("PSEUDO_ADIABATIC_POTENTIAL_TEMPERATURE__ISOBARIC")) return true;
        if (label.contains("POTENTIAL_VORTICITY__ISOBARIC")) return true;
        if (label.contains("TEMPERATURE__GROUND_OR_WATER_SURFACE")) return true;
        if (label.contains("TEMPERATURE__ISOBARIC_SURFACE")) return true;
        if (label.contains("U_COMPONENT_OF_WIND__ISOBARIC_")) return true;
        if (label.contains("U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY")) return true;
        if (label.contains("V_COMPONENT_OF_WIND__ISOBARIC_SURFACE")) return true;
        if (label.contains("V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY")) return true;
        if (label.contains("GEOPOTENTIAL__ISOBARIC_SURFACE___")) return true;
        return false;
    }
}