import java.text.SimpleDateFormat;
import java.text.FieldPosition;
import java.util.Date;
import java.util.TimeZone;
class GetCoveragePath{  // un path pour faire une requête getCoverage au WCS
    private String getCoveragePath;
    public GetCoveragePath (String getCoveragePath) {
        this.getCoveragePath=getCoveragePath;
    }public void affiche(){
        System.out.println("je suis le getCoveragePath : "+ this.getCoveragePath);
    }
    public String getCoveragePath(){
        return this.getCoveragePath;
    }
    public String getStringDateDePrevision(){
        int index=this.getCoveragePath.indexOf("time(");
        String rep=this.getCoveragePath.substring(index+5,index+25);
        return rep;
    }
    public Date getDateDeLaPrevision() throws Exception {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
        Date rep = sdf.parse(this.getStringDateDePrevision());
        return rep;
    }
    public long getTSInMiliDateDeLaPrevision() throws Exception {
        return (this.getDateDeLaPrevision().getTime());
    }
    public double getDelaiDeLaPrevision() throws Exception {  // calcul l'age en heure
       long now=new Date().getTime();  // cette heure est celle du serveur qui n'est pas forcement l'heure UTC !
       int decal=TimeZone.getDefault().getOffset(now);  // calcul du décalage par rapport à UTC
       now=now-decal; // calcul de l'heure actuelle UTC
       double delai=(this.getTSInMiliDateDeLaPrevision()-now)/1000./3600.;
       return (delai);
    }
    public String getNomDeLaVariable(){
        int index=this.getCoveragePath.indexOf("coverageId=");
        String rep=this.getCoveragePath.substring(index+11,index+40);
        return rep;
    }
    public boolean estUnePrevision() throws Exception {
        if (this.getDelaiDeLaPrevision() >0) {
            return true;
        }
        else {
            return false;
        }
    }
}