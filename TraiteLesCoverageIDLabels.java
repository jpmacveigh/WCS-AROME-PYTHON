import java.util.HashMap;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.concurrent.TimeUnit;
import java.lang.Runtime;
class TraiteLesCoverageIDLabels {
    public static void main (String[] arg) throws Exception {
        //String coverageIDLabel = "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000___2017-08-25T12.00.00Z";
        //String coverageIDLabel="POTENTIAL_VORTICITY__ISOBARIC_SURFACE___2017-08-26T00.00.00Z";
        //String coverageIDLabel="MINIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___2017-08-29T06.00.00Z";
        //String resolution = "0025";
        String resolution =arg[0];  // la résolution ("OO25 ou "001") est passée en premier argument
        String fichDesCoverageIDlabel=arg[1];
        //getWCSCapabilities(resolution);
        BufferedReader br = new BufferedReader(new FileReader(fichDesCoverageIDlabel));
        String line;
        long nb=0;
        String coverageIDLabel;
        long nbLabel=0;
        long nbLabelTraites=0;
        while ((coverageIDLabel = br.readLine()) != null) {  // lectures des lignes du fichier WCScapabilities
            nbLabel=nbLabel+1;
            System.out.println(nbLabel+"  "+coverageIDLabel);
            CoverageIDLabel label= new CoverageIDLabel(coverageIDLabel);
            //label.affiche();
            //System.out.println("mon nom : "+label.getName());
            //System.out.println("ma date : "+label.getStringDate());
            //System.out.println("mon suffixe : "+label.getSuffixe());
            //System.out.println("mon TS en milisecondes : "+label.getTSInMiliDate());
            if (label.getCumul()!= null) System.out.println("mon cumul : "+label.getCumul());
            double age=label.getAge();
            //System.out.println("mon age (heures) : "+age);
            //System.out.println("suis-je futur ? "+label.isFutur());
            //System.out.println("A ignorer : "+label.aIgnorer());
            if ((age<=8)&&(!label.aIgnorer()))  {  // on ne traite que les certains coverageIDLabel de moins de 8 heures d'age 
                nbLabelTraites=nbLabelTraites+1;
                //long echeance=36000;
                //System.out.println("echeance (sec) : "+echeance+" date prevision : "+label.getDateDeLaPrevision(echeance));
                CoverageID cov=new CoverageID(label,resolution);
                System.out.println("Labels traités: "+nbLabelTraites+"   "+cov.getDescribeCoveragePath());
                HashMap<String,String[]> lesCoordonnees=cov.getLesCoordonnees();
                for (String key : lesCoordonnees.keySet()){
                    System.out.println(key);
                    System.out.println(lesCoordonnees.get(key).length);
                    for (String coef : lesCoordonnees.get(key)){
                        //System.out.println(coef);    
                    }
                }
                ArrayList<GetCoveragePath> lesPaths=cov.getLesGetCoveragePaths(50.,51.,3.,4.);
                int nbPrevision=0;
                for (GetCoveragePath path : lesPaths){
                    if (path.estUnePrevision() ){  // on de traite que les prévision (date future)
                        nbPrevision=nbPrevision+1;
                        System.out.println(nbPrevision+" calcul des previsions avec :"+path.getCoveragePath());
                        String commande = "./getEtAnalyseCoverage.sh "+path.getCoveragePath()+" "+path.getNomDeLaVariable();
                        Runtime.getRuntime().exec(commande);
                        TimeUnit.MILLISECONDS.sleep(500);
                        
                    }
                }
                System.out.println("nb de paths calculés : "+lesPaths.size());
                //TimeUnit.SECONDS.sleep(1);  // pour laisser le temps au serveur Inspire de MF de se retrouner
            }
        }
    }
    /*
    static private String getWCSCapabilities(String resolution) throws Exception {
        String path="https://geoservices.meteofrance.fr/services/MF-NWP-HIGHRES-AROME-";
        path=path+resolution+"-FRANCE-WCS?request=GetCapabilities&version=1.3.0&service=WCS&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__";
        System.out.println ("path pour getCapabilities : "+path);
        String resultGetWCSCapabilities=GetUrl.get(path);  // requete getCapabilities au WCS de MF pour le modèle AROME
        return resultGetWCSCapabilities;
    }
    */
    static void lireLesCapabilities() throws Exception {
        BufferedReader br = new BufferedReader(new FileReader("../WCScapabilities"));
        String line;
        long nb=0;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
            nb=nb+1;
        }
        br.close();
        System.out.println("nb de CoverageIDLabel lus : "+nb);
    }
}