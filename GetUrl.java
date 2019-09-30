import java.io.IOException;
import java.net.URL;
import java.io.BufferedReader;
//import java.net.URLConnection;
import java.net.HttpURLConnection;
import java.io.InputStreamReader;
import java.lang.StackTraceElement;
import java.util.concurrent.TimeUnit;
import java.lang.InterruptedException;
class GetUrl{
    public static Object[] get(String url) throws IOException,InterruptedException {
        Object[] rep=  new Object[2];
        String source ="";
        int codeRetourHTTP=503;
        BufferedReader in=null;
        HttpURLConnection con=null;
        URL ur = new URL(url);
        //URLConnection con = ur.openConnection();
        while ((codeRetourHTTP==503)||(codeRetourHTTP==404)){  // boucle après attente d'une seconde quand serveur renvoi code 503 (serveur pas prêt)
            con =(HttpURLConnection) ur.openConnection();
            codeRetourHTTP = con.getResponseCode();
            System.out.println("retour con : "+codeRetourHTTP);
            if ((codeRetourHTTP==503)||(codeRetourHTTP==404)) TimeUnit.SECONDS.sleep(1);  // attendre une seconde avant de boucler
        }
        try{
            in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            while ((inputLine = in.readLine()) != null) source +=inputLine;
        }
        catch (IOException e){
            codeRetourHTTP = con.getResponseCode();
            System.out.println ("retour HTTP : "+codeRetourHTTP);
        }
        //in.close();
        rep[0]=source;
        rep[1]=codeRetourHTTP;
        if (codeRetourHTTP==404){
            System.out.println("retour 404 pour : "+url);
        }
        return rep;
    }
}