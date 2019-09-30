import java.util.ArrayList;
import java.util.Arrays;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.HashMap;
import java.util.Set;
import java.util.Iterator;
import java.lang.Long;
import java.text.DecimalFormat;
class CoverageID {
    private CoverageIDLabel coverageIDLabel;
    private String resolution;  // "0025" ou "001"
    private String describedCoverage;
    private HashMap <String,String[]> lesCoordonnees=new HashMap<String,String[]>();
    private ArrayList<String> lesPathsPourGetCoverage =new ArrayList<String>();
    public CoverageID(CoverageIDLabel coverageIDLabel,String resolution) throws Exception { // constructeur
        this.coverageIDLabel=coverageIDLabel;
        this.resolution=resolution;
        this.describedCoverage=this.getDescribedCoverage();  // requete "describecoverage" au WCS
        this.construireLesAxes();
    }
    
    public String getDescribeCoveragePath(){  // calcul le path pour une requette describeCoverage pour ce CoverageID
        String model="MF-NWP-HIGHRES-AROME-"+this.resolution+"-FRANCE-WCS";
        String path="https://geoservices.meteofrance.fr/services/"+model+"?SERVICE=WCS&version=2.0.1&REQUEST=DescribeCoverage&coverageID=";
        path=path+this.coverageIDLabel.getCoverageIDLabel()+"&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"; 
        return (path); 
    }
    private String getDescribedCoverage() throws Exception {  // emet une requette describeCoverage au WCS de MF pour ce CoverageID
        String xml="";
        Object[] retour=new Object[2];
        retour = GetUrl.get(this.getDescribeCoveragePath());
        xml=(String)retour[0];
        int codeHttp=(int)retour[1];
        System.out.println ("code retour Http getDescribeCoverage : "+codeHttp);
        return (xml);
    }
    private void construireLesAxes() throws Exception {  // analyse le describedCoverage reçu
        String xml=this.describedCoverage;
        String tagAxes="<gml:axisLabels>";
        String tagFinAxes="</gml:axisLabels>";
        Pattern p = Pattern.compile(tagAxes+".+"+tagFinAxes);
		Matcher m = p.matcher(xml);
		ArrayList<String> lesAxes=new ArrayList<String>();
		while(m.find()) {
			//System.out.println("\nrecherche nom des axes : "+m.group());
			String trouv=m.group();
			trouv=trouv.replace(tagAxes,"");
			trouv=trouv.replace(tagFinAxes,"");
			trouv=trouv.replace("  "," ");
			String[] lesAxesBruts = trouv.split(" ");
			for (int i=1;i<=lesAxesBruts.length-2;i++){  // on enlève les deux premiers (lat et lon)
			    lesAxes.add(lesAxesBruts[i+1]);
			}
			System.out.println(lesAxes.size());
			for (String axe:lesAxes){
	            System.out.println(axe);
			}
		}
		String tagCoeff="<gmlrgrid:coefficients>";
        String tagFinCoeff="</gmlrgrid:coefficients>";
        p = Pattern.compile(tagCoeff+"(\\d+| )+"+tagFinCoeff);
		m = p.matcher(xml);
		int rang=0;
		while(m.find()) {
			//System.out.println("\nrecherche coef : "+m.group());
			String trouv=m.group();
			trouv=trouv.replace(tagCoeff,"");
			trouv=trouv.replace(tagFinCoeff,"");
			String[] lesCoeff = trouv.split(" ");
			System.out.println(lesCoeff.length);
			for (int i=0;i<=lesCoeff.length-1;i++){
	            String coeff=lesCoeff[i];
	            //System.out.println(coeff); 
	            if (lesAxes.get(rang).equals("time")) { // pour l'axe "time", calculer la date de la prevision
	               long echeance= Long.parseLong(coeff);
	               coeff=this.coverageIDLabel.getDateDeLaPrevision(echeance);
	            }
	            String subset="&subset="+lesAxes.get(rang)+"("+coeff+")";
	            lesCoeff[i]=subset;
			}
			this.lesCoordonnees.put(lesAxes.get(rang),lesCoeff);  // les coefficients indicés par les nom de l'axe
			rang=rang+1;
		}
    }
    public HashMap<String,String[]> getLesCoordonnees(){
        return this.lesCoordonnees;
    }
    public ArrayList<GetCoveragePath> getLesGetCoveragePaths(double latiSud,double latiNord,double longiOuest,double longiEst){ // cacul la liste des getCoveragePaths possible pour ce CoverageID
        ArrayList<String> rep = new ArrayList<String>();
        int nbAxes=this.lesCoordonnees.size();  // nombre d'axes : 1 ou 2 pour MF : time et une height ou un pressure)
        System.out.println("nb d'axes : "+nbAxes);
        Set<String> lesNomsDesAxes=this.lesCoordonnees.keySet();
        Iterator iter=lesNomsDesAxes.iterator();
        rep=new ArrayList(Arrays.asList(this.lesCoordonnees.get(iter.next())));
        rep=(this.boucle(rep,iter));
        // https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__
        // /MF-NWP-HIGHRES-AROME-0025-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage
        // &format=image/tiff&coverageId=GEOPOTENTIAL__ISOBARIC_SURFACE___2017-08-29T06.00.00Z
        // &subset=lat(50.0,51.0)&subset=long(3.0,4.0)&subset=pressure(100)&subset=time(2017-08-29T15:00:00Z)
        DecimalFormat nf = new DecimalFormat() ;
        nf.setMaximumFractionDigits(3); // la tu auras au plus 3 chiffres apres la virgule
        String latitude  = "&subset=lat("+nf.format(latiSud)+","+nf.format(latiNord)+")";
        String longitude = "&subset=long("+nf.format(longiOuest)+","+nf.format(longiEst)+")";
        String domaineGeo=latitude+longitude;
        String path="https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__/MF-NWP-HIGHRES-AROME-";
        path=path+resolution+"-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=";
        path=path+this.coverageIDLabel.getCoverageIDLabel();
        path=path+domaineGeo;
        ArrayList<GetCoveragePath> lesPaths = new ArrayList<GetCoveragePath>();
        for (String fin : rep){
           lesPaths.add(new GetCoveragePath(path+fin)); 
        }
        return lesPaths;
        
    }
    private ArrayList<String> boucle (ArrayList<String> list,Iterator iter){  // boucle récursive sur les axes
            if (!iter.hasNext()) return (list);
            ArrayList<String> newlist=new ArrayList<String>();
            String[] prochain=this.lesCoordonnees.get(iter.next());
            for (String str : list){
                for(String strnew : prochain){
                    newlist.add(str+strnew);
                }
            }
            return(boucle(newlist,iter));
     }
}