import com.ib.client.*;
import java.sql.*;

import java.io.PrintWriter;
import java.io.File;

import java.util.Calendar;
import java.text.SimpleDateFormat;

import java.text.*;

public class GetIBData implements EWrapper{

	static String Symbol = "SPY";
	static String Period = "1 D";
	static String Unit = "5 min";
	static String EndTime;

	static PrintWriter Writer;
	static String DataPath = "/opt/co/PerlProgramming/stock/data";
	
	static int Disconnect = 0;

	EClientSocket m_client;

	public static final String DATE_FORMAT_NOW = "yyyyMMdd HH:mm:ss";

	GetIBData() {

		m_client = new EClientSocket(this);

		m_client.eConnect("ib_host", 7496, 1);

		Contract contract;
		contract = new Contract();

		contract.m_symbol	= Symbol;
		contract.m_secType	= "STK";
		contract.m_expiry	= "";
		contract.m_right	= "";
		contract.m_multiplier	= "";
		contract.m_exchange	= "SMART";
		contract.m_primaryExch	= "NYSE";
		contract.m_currency	= "USD";
		contract.m_localSymbol	= "";

		String endTime;
		int useRTH = 0;
		int formatDate = 1;
		
		if (EndTime=="") {
			Calendar cal = Calendar.getInstance();
			SimpleDateFormat sdf = new SimpleDateFormat(DATE_FORMAT_NOW);
			endTime = sdf.format(cal.getTime());
		} else {
			endTime = EndTime;
		}

		String[] dateArray = endTime.split("\\s+");
		String[] unitArray = Unit.split("\\s+");
		if (unitArray[1].equals("secs")) {
			unitArray[1] = "sec";
		} else if (unitArray[1].equals("mins")) {
			unitArray[1] = "min";
		}

		try {

			if (Symbol.indexOf(" ")>0) {
				String [] symbols = Symbol.split(" ");
				for (int i=0; i<symbols.length; i++) {
					if (i==(symbols.length - 1)) {
						Disconnect = 1;
					}
					File file = new File(symbols[i] + "_" + dateArray[0] + "." + unitArray[1] + unitArray[0]);
					Writer = new PrintWriter(file);
					contract.m_symbol = symbols[i];
					m_client.reqHistoricalData(0, contract, endTime, Period, Unit, "TRADES", useRTH, formatDate);
				}
			} else {
				Disconnect = 1;
				File file = new File(Symbol + "_" + dateArray[0] + "." + unitArray[1] + unitArray[0]);
				Writer = new PrintWriter(file);
				m_client.reqHistoricalData(0, contract, endTime, Period, Unit, "TRADES", useRTH, formatDate);
			}

		} catch (Exception e) {

			e.printStackTrace();

		}

	}

	public static void main(String args[]) {

		System.out.println("Testing IB API.");

		if (args.length==0) {
			System.out.println("java GetIBData <symbol> <period> <time unit> [end datetime]");
			System.out.println("Example:");
			System.out.println("\tjava GetIBData SPY '1 D' '1 min' '20140414 20:00:00 EST'");
			System.exit(1);
		}
		
		Symbol = args[0];
		Period = args[1];
		Unit = args[2];

		if (args.length==4) {
			EndTime = args[3];
		} else {
			EndTime = "";
		}

		GetIBData myMain;

		myMain= new GetIBData();
		
		System.out.println("Done.");

	}

	public void historicalData(int reqId, String date, double open, double high, double low, double close, int volume, int tradesCount, double WAP, boolean hasGaps) {
		if (date.startsWith("finished")) {
			// System.out.println("Exiting ...");
			if (Disconnect==1) {
				m_client.eDisconnect();
				Writer.close();
			}
		}
		if (volume==-1) {
			// System.out.println("Date: "+date+" Open: "+open+" High: "+high+" Low: "+low+" Close: "+close+" WAP: "+WAP+" Volume: "+volume);
			Disconnect = 1;
		} else {
			// System.out.printf("%s\t%s\t%f\t%f\t%f\t%f\t%d\t%d\t%f\t\n", Symbol, date, open, high, low, close, volume, tradesCount, WAP);
			int gap = (hasGaps) ? 1 : 0;
			if (volume>0) {

				DecimalFormat df = new DecimalFormat("0.#####");
				String o = df.format(Double.valueOf(open));
				String h = df.format(Double.valueOf(high));
				String l = df.format(Double.valueOf(low));
				String c = df.format(Double.valueOf(close));
				String w = df.format(Double.valueOf(WAP));

				String dt = date.replace("  ", " ");

				Writer.printf("%s\t%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s\t%d\n", Symbol, dt, o, h, l, c, volume, tradesCount, w, gap);
			}
		}
	}

	public void tickPrice(int tickerId, int field, double price,int canAutoExecute ) {
	}

	public void tickSize(int tickerId, int field, int size) {
	}

	public void orderStatus( int orderId, String status, int filled, int remaining,
		double avgFillPrice, int permId, int parentId, double lastFillPrice, int clientId) {
	}

	public void openOrder(int orderId, Contract contract, Order order) {
	}

	public void error(String str) {
	}

	public void connectionClosed() {
	}

	public void updateAccountValue(String key, String value, String currency, String accountName) {
	}

	public void updatePortfolio(Contract contract, int position, double marketPrice, double marketValue) {
	}

	public void updateAccountTime(String timeStamp)	{
	}

	public void nextValidId(int orderId) {
	}

	public void contractDetails(ContractDetails contractDetails) {
	}

	public void execDetails(int orderId, Contract contract, Execution execution) {
	}

	public void error(int id, int errorCode, String errorMsg) {
		System.out.println("Error: "+errorMsg);
		if ((	errorMsg.equals("No security definition has been found for the request") || 
			errorMsg.indexOf(" is ambiguous") > 0 || 
			errorMsg.indexOf("invalid step") > 0 || 
			errorMsg.indexOf("pacing violation") > 0 || 
			errorMsg.indexOf("No market data permissions") > 0 || 
			errorMsg.indexOf("returned no data") > 0) && Disconnect == 1) {
			m_client.eDisconnect();
			Writer.close();
		}
	}

	public void updateMktDepth(int tickerId, int position, int operation, int side, double price, int size) {
	}

	public void updateMktDepthL2(int tickerId, int position, String marketMaker, int operation, int side, double price, int size) {
	}

	public void updateNewsBulletin( int msgId, int msgType, String message, String origExchange){
	}

	public void managedAccounts( String accountsList){
	}

	public void receiveFA(int faDataType, String xml){
	}

	public void intradayData(int reqId, String date, double open, double high, double low, double close, int volume, double WAP, boolean hasGaps){
	}

	public void updatePortfolio(Contract contract, int position, double marketPrice, double marketValue, double averageCost, double unrealizedPNL, double realizedPNL, String accountName){
	}

	public void scannerData(int reqId, int rank, ContractDetails contractDetails, String distance, String benchmark, String projection,String temp){

	}

	public void scannerParameters(String xml){
	}

	public   void bondContractDetails(ContractDetails contractDetails){
	}

	public void tickEFP(int x,int y,double m,String str1,double n,int k,String str2,double l ,double v) {
	}

	public void tickString(int a,int b,String c) {
	}

	public void tickGeneric(int a,int b,double c) {
	}

	public void tickOptionComputation(int a,int b,double c ,double d,double e,double f) {
	}

	public void error(Exception e) {
	}

	public void tickSnapshotEnd(int tickerId) {
	}

	public void deltaNeutralValidation(int reqId, UnderComp underComp) {
	}

	public void fundamentalData(int reqId, String data) {
	}

	public void currentTime(long time) {
	}

	public void realtimeBar(int reqId, long time, double open, double high, double low, double close, long volume, double wap, int count) {
	}

	public void scannerDataEnd(int reqId) {
	}

	public void execDetailsEnd(int reqId) {
	}

	public void contractDetailsEnd(int reqId) {
	}

	public void bondContractDetails(int reqId, ContractDetails contractDetails) {
	}

	public void contractDetails(int reqId, ContractDetails contractDetails) {
	}

	public void accountDownloadEnd(String accountName) {
	}

	public void openOrderEnd() {
	}

	public void openOrder( int orderId, Contract contract, Order order, OrderState orderState) {
	}

	public void orderStatus( int orderId, String status, int filled, int remaining,
		double avgFillPrice, int permId, int parentId,
		double lastFillPrice, int clientId, String whyHeld) {
	}
}
