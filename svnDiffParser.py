# -*- coding: utf-8 -*-
from ptk.parser import LRParser, production, leftAssoc, nonAssoc
from ptk.lexer import ReLexer, token

class Parser(LRParser, ReLexer):
    
    def __init__(self):
        LRParser.__init__(self)
        ReLexer.__init__(self)
        self.lineNum = 0

    def ignore(self, char):
        return False

    def parse(self, content):
        self.lineNum = 0
        return ReLexer.parse(self, content)


    @token(ur"^\n$")
    def EMPTYLINE(self, tok):
        self.lineNum += 1
        pass

    @token(ur"^((Index)|(Modified)|(Deleted)|(Added)|(Copied)): [^\n]*(\n|$)")
    def FILENAME(self, tok):
#        print 'fileName:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass

    @token(ur"^=+(\n|$)")
    def HRULE(self, tok):
#        print 'hrule:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass

    @token(ur"^ [^\n]*(\n|$)")
    def NORMALlINE(self, tok):
#        print 'normalLine:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass

    @token(ur"^--- [^\n]*(\n|$)")
    def SRClINE(self, tok):
#        print 'srcLine:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass

    @token(ur"^\+\+\+ [^\n]*(\n|$)")
    def DESTlINE(self, tok):
#        print 'DESTlINE:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass


    @token(ur"^@@ [^\n]+ @@(\n|$)")
    def BLOCKDESC(self, tok):
#        print 'block desc:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass

    @token(ur"^[\+-\\][^\n]*(\n|$)")
    def OPlINE(self, tok):
#        print 'opline:', tok.value
        tok.value = (tok.value, self.lineNum)
        self.lineNum += 1
        pass

    @production(ur'diff->diffFile+<files>')
    def diff(self, files):
        return files
        pass

#    @production(ur'diffFile->FILENAME HRULE SRClINE DESTlINE diffBlocks')
#    @production(ur'diffFile->FILENAME HRULE SRClINE DESTlINE BLOCKLINE')
#    @production(ur'diffFile->')
    @production(ur'diffFile->FILENAME<path> HRULE SRClINE DESTlINE diffBlocks<fileDiff>')
    def diffFile(self, path, fileDiff):
        return path, fileDiff
        pass

    @production(ur'diffBlocks->diffBlock+<blocks>')
    def diffBlocks(self, blocks):
        return ''.join(blocks)
        pass

    @production(ur'diffBlock->BLOCKDESC<desc> blockBody<body> EMPTYLINE?')
    def diffBlock(self, desc, body):
        return desc[0] + body
        pass
#
    @production(ur'blockBody->blockBodyLine+<lines>')
    def blockBody(self, lines):
        return ''.join(lines)
        pass

    @production(ur'blockBodyLine-> NORMALlINE<norm> | OPlINE<op>')
    def blockBodyLine(self, **argv):
        norm = argv.pop('norm', None)
        op = argv.pop('op', None)
        if None != norm:
            return norm[0]
        else:
            return op[0]
        pass

    def newSentence(self, sentence):
        self.ret = sentence
        return sentence




if __name__ == '__main__':
    content = ur"""Index: gervs-dao/.classpath
===================================================================
--- gervs-dao/.classpath	(revision 4194)
+++ gervs-dao/.classpath	(working copy)
@@ -1,37 +1,36 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.nondependency" value=""/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: gervs-dao/src/main/resources/mybatis/masterdata/MdFloorMapper.xml
===================================================================
--- gervs-dao/src/main/resources/mybatis/masterdata/MdFloorMapper.xml	(revision 4194)
+++ gervs-dao/src/main/resources/mybatis/masterdata/MdFloorMapper.xml	(working copy)
@@ -26,4 +26,22 @@
 			f.BUILDINGID = #{BUILDINGID}
 			and f.ENABLE = 1
 	</select>
-</mapper>
\ No newline at end of file
+	<select id = "listFloorDesc" parameterType="pd" resultType="pd">
+		SELECT
+		  M.CITY
+			  || ', '
+			  || M.DMALLNAME
+			  || ', '
+			  || F.BUILDINGNUM FLOORDESC,
+		  M.MALLID,
+		  F.FLOORID
+		FROM
+		  MD_FLOOR F
+		LEFT JOIN MD_MALL M
+		ON
+		  F.MALLID = M.MALLID
+		WHERE
+		  F.ENABLE   = 1
+		AND M.ENABLE = 1
+	</select>
+</mapper>
Index: gervs-job/.classpath
===================================================================
--- gervs-job/.classpath	(revision 4194)
+++ gervs-job/.classpath	(working copy)
@@ -1,37 +1,36 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.dependency" value="/WEB-INF/lib"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: gervs-job/.settings/org.eclipse.m2e.core.prefs
===================================================================
--- gervs-job/.settings/org.eclipse.m2e.core.prefs	(revision 4194)
+++ gervs-job/.settings/org.eclipse.m2e.core.prefs	(working copy)
@@ -1,4 +1,4 @@
-activeProfiles=dev
+activeProfiles=
 eclipse.preferences.version=1
 resolveWorkspaceProjects=true
 version=1
Index: gervs-service/.classpath
===================================================================
--- gervs-service/.classpath	(revision 4194)
+++ gervs-service/.classpath	(working copy)
@@ -1,37 +1,36 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.nondependency" value=""/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: gervs-service/src/main/java/com/gervs/facade/bvmmap/BvmBaseFacade.java
===================================================================
--- gervs-service/src/main/java/com/gervs/facade/bvmmap/BvmBaseFacade.java	(revision 4194)
+++ gervs-service/src/main/java/com/gervs/facade/bvmmap/BvmBaseFacade.java	(working copy)
@@ -146,6 +146,10 @@
 		if (BoothConstants.YESNO_STRING_YES.equals(dimensionDto.getIsneedcontrol())) {
 			secrityFloorList = dimensionDto.getFlooridList();
 		}
+		logger.debug("getIsneedcontrol");
+		logger.debug(dimensionDto.getIsneedcontrol());
+		logger.debug("secrityFloorList");
+		logger.debug(secrityFloorList);
 		// 获取楼层信息
 		int floorCount = 0;
 		FLOORID = "";
Index: gervs-service/src/main/java/com/gervs/facade/mail/MailConfigFacade.java
===================================================================
--- gervs-service/src/main/java/com/gervs/facade/mail/MailConfigFacade.java	(revision 4194)
+++ gervs-service/src/main/java/com/gervs/facade/mail/MailConfigFacade.java	(working copy)
@@ -37,6 +37,15 @@
 	private JsonObject mailConfig;
 	private String settingFilePath;
 
+	private synchronized JsonObject getMailConfig()
+	{
+		if (mailConfig == null)
+		{
+			initConfig();
+		}
+		return mailConfig;
+	}
+
 	private synchronized void initConfig()
 	{
 		try
@@ -167,4 +176,62 @@
 		saveConfig();
 		return listRecipients(mallId);
 	}
+
+	public synchronized String setSMTPHost(String host) throws Exception
+	{
+		getMailConfig().addProperty("host", host);
+		saveConfig();
+		return host;
+	}
+
+	public synchronized String getSMTPHost() throws Exception
+	{
+		return getMailConfig().get("host").getAsString();
+	}
+
+	public synchronized String setFromAddress(String address) throws Exception
+	{
+		getMailConfig().addProperty("address", address);
+		saveConfig();
+		return address;
+	}
+
+	public synchronized String getFromAddress() throws Exception
+	{
+		return getMailConfig().get("address").getAsString();
+	}
+
+	public synchronized String setPassword(String password) throws Exception
+	{
+		getMailConfig().addProperty("password", password);
+		saveConfig();
+		return password;
+	}
+
+	public synchronized String getPassword() throws Exception
+	{
+		return getMailConfig().get("password").getAsString();
+	}
+
+	public synchronized String setMailPort(String port) throws Exception
+	{
+		getMailConfig().addProperty("port", port);
+		saveConfig();
+		return port;
+	}
+
+	public synchronized String getMailPort() throws Exception
+	{
+		return getMailConfig().get("port").getAsString();
+	}
+
+	public synchronized String getMailParams() throws Exception
+	{
+		JsonObject ret = new JsonObject();
+		ret.add("host", getMailConfig().get("host"));
+		ret.add("address", getMailConfig().get("address"));
+		ret.add("password", getMailConfig().get("password"));
+		ret.add("port", getMailConfig().get("port"));
+		return ret.toString();
+	}
 }
Index: gervs-service/src/main/java/com/gervs/facade/themeanalyze/businessindex/MallBoothVacancyFacade.java
===================================================================
--- gervs-service/src/main/java/com/gervs/facade/themeanalyze/businessindex/MallBoothVacancyFacade.java	(revision 4194)
+++ gervs-service/src/main/java/com/gervs/facade/themeanalyze/businessindex/MallBoothVacancyFacade.java	(working copy)
@@ -142,16 +142,16 @@
 		pData.put("MALLID", MALLPD.getStringSafe("MALLID"));
 		String DMALLNAME = MALLPD.getStringSafe("DMALLNAME");
 		String USERLEVEL = pData.getStringSafe("USERLEVEL");
-		List<PageData> sreachMallBoothVacanctList=null;
+		List<PageData> searchMallBoothVacanctList=null;
 		if(USERLEVEL.equals("1")){
-			sreachMallBoothVacanctList = this.sreachMallBoothVacanctList(pData);
+			searchMallBoothVacanctList = this.searchMallBoothVacanctList(pData);
 		}else if(USERLEVEL.equals("4")){
-			sreachMallBoothVacanctList = this.sreachMallBoothVacanctList(pData);
+			searchMallBoothVacanctList = this.searchMallBoothVacanctList(pData);
 		}
 		double CURRALLAREA = 0;
 		double CURRRENTEDAREA =0;
 		double CURRVACANCYRATE=0;
-		for (PageData pageData : sreachMallBoothVacanctList) {
+		for (PageData pageData : searchMallBoothVacanctList) {
 			String all = pageData.getStringSafe("CURRALLAREA");
 			String RENTED = pageData.getStringSafe("CURRRENTEDAREA");
 			String rate = pageData.getStringSafe("CURRVACANCYRATE");
@@ -179,7 +179,7 @@
 		pData.put("MALLID", MALLPD.getStringSafe("MALLID"));
 		pData.put("CITY", MALLPD.getStringSafe("CITY"));
 		pData.put("PROVINCE", MALLPD.getStringSafe("PROVINCE"));
-		pData.put("sreachMallBoothVacanctList", sreachMallBoothVacanctList);
+		pData.put("searchMallBoothVacanctList", searchMallBoothVacanctList);
 		return pData;
 	}
 	
@@ -189,9 +189,9 @@
 	 * @return
 	 * @throws Exception
 	 */
-	public List<PageData> sreachMallBoothVacanctList(PageData pd) throws Exception {
+	public List<PageData> searchMallBoothVacanctList(PageData pd) throws Exception {
 		DecimalFormat df=new DecimalFormat("######0.00"); 
-		List<PageData>  sreachMallBoothVacanctList= new ArrayList<PageData>();
+		List<PageData>  searchMallBoothVacanctList= new ArrayList<PageData>();
 		List<PageData> BUILDINGLIST = (List<PageData>) pd.get("BUILDINGLIST");
 		for (PageData buildingPd : BUILDINGLIST) {
 			List<PageData> floorList = (List<PageData>) buildingPd.get("FLOORLIST");
@@ -224,10 +224,10 @@
 				String BUILDINGNAME = buildingPd.getStringSafe("BUILDINGNAME");
 				boothPd.put("FLOORNAME", FLOORNAME);//楼层名
 				boothPd.put("BUILDINGNAME", BUILDINGNAME);//楼栋名称
-				sreachMallBoothVacanctList.add(boothPd);
+				searchMallBoothVacanctList.add(boothPd);
 			}
 		}
-		return sreachMallBoothVacanctList;
+		return searchMallBoothVacanctList;
 	}
 
 	/**
Index: gervs-service/src/main/java/com/gervs/service/masterdata/MdFloorService.java
===================================================================
--- gervs-service/src/main/java/com/gervs/service/masterdata/MdFloorService.java	(revision 4194)
+++ gervs-service/src/main/java/com/gervs/service/masterdata/MdFloorService.java	(working copy)
@@ -115,4 +115,12 @@
 		List<PageData> floorList = this.sqlSessionTemplate.<PageData> selectList("MdFloorMapper.listByBuildingId", firstBuilding);
 		return floorList;
 	}
-}
\ No newline at end of file
+
+	/**
+	 * 获得楼层描述列表
+	 */
+	public List<PageData> listFloorDesc() {
+		List<PageData> floorList = this.sqlSessionTemplate.<PageData> selectList("MdFloorMapper.listFloorDesc", new PageData());
+		return floorList;
+	}
+}
Index: gervs-service/src/main/java/com/gervs/service/system/login/LoginService.java
===================================================================
--- gervs-service/src/main/java/com/gervs/service/system/login/LoginService.java	(revision 4194)
+++ gervs-service/src/main/java/com/gervs/service/system/login/LoginService.java	(working copy)
@@ -300,6 +300,8 @@
 
 				mlddd.setFlooridList(floorids);
 			}
+			logger.debug("Const.SESSION_DATA_PERMISSIONS_MF");
+			logger.debug(mlddd);
 			session.setAttribute(Const.SESSION_DATA_PERMISSIONS_MF, mlddd);
 		}
 
Index: gervs-util/.classpath
===================================================================
--- gervs-util/.classpath	(revision 4194)
+++ gervs-util/.classpath	(working copy)
@@ -1,32 +1,31 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.nondependency" value=""/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: gervs-web/.classpath
===================================================================
--- gervs-web/.classpath	(revision 4194)
+++ gervs-web/.classpath	(working copy)
@@ -1,37 +1,36 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.dependency" value="/WEB-INF/lib"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: gervs-web/pom.xml
===================================================================
--- gervs-web/pom.xml	(revision 4194)
+++ gervs-web/pom.xml	(working copy)
@@ -169,6 +169,13 @@
 			<artifactId>cxf-rt-rs-client</artifactId>
 		</dependency>
 
+		<!-- https://mvnrepository.com/artifact/javax.mail/mail -->
+		<dependency>
+			<groupId>javax.mail</groupId>
+			<artifactId>mail</artifactId>
+			<version>1.4</version>
+		</dependency>
+
 		<!-- Apache shiro -->
 		<dependency>
 			<groupId>org.apache.shiro</groupId>
Index: gervs-web/src/main/java/com/gervs/controller/MailController.java
===================================================================
--- gervs-web/src/main/java/com/gervs/controller/MailController.java	(revision 4194)
+++ gervs-web/src/main/java/com/gervs/controller/MailController.java	(working copy)
@@ -1,14 +1,22 @@
 package com.gervs.controller;
 
+import java.text.SimpleDateFormat;
+import java.util.Date;
 import java.util.HashMap;
 import java.util.ArrayList;
 import java.util.List;
 import java.util.Map;
+import java.util.Properties;
 
 import javax.annotation.Resource;
 import javax.servlet.http.HttpServletRequest;
 import javax.servlet.http.HttpServletResponse;
 
+import javax.mail.Message;
+import javax.mail.internet.MimeMessage;
+import javax.mail.internet.InternetAddress;
+import com.sun.mail.smtp.SMTPTransport;
+
 import org.springframework.beans.factory.annotation.Autowired;
 import org.springframework.stereotype.Controller;
 import org.springframework.web.bind.annotation.RequestMapping;
@@ -16,6 +24,7 @@
 import org.springframework.web.bind.annotation.ResponseBody;
 import org.springframework.web.servlet.ModelAndView;
 
+
 import org.apache.shiro.SecurityUtils;
 import org.apache.shiro.session.Session;
 import org.apache.shiro.subject.Subject;
@@ -28,8 +37,12 @@
 import com.gervs.controller.base.BaseController;
 import com.gervs.entity.Page;
 import com.gervs.facade.mail.MailConfigFacade;
+import com.gervs.facade.themeanalyze.businessindex.ContratMaturityDayFacade;
+import com.gervs.service.masterdata.MdFloorService;
 
 import com.gervs.util.Const;
+import com.gervs.util.PageData;
+import com.gervs.util.DateUtil;
 
 @RequestMapping("/mail")
 @Controller
@@ -37,6 +50,11 @@
 {
 	@Autowired
 	private MailConfigFacade mailConfigFacade;
+	@Autowired
+	protected MdFloorService mdFloorService;
+	@Autowired
+	private ContratMaturityDayFacade contratMaturityDayFacade;
+
 	private String getCurrentMallId() throws Exception 
 	{
 		Subject currentUser = SecurityUtils.getSubject();
@@ -190,5 +208,174 @@
 			return "请求参数错误";
 		}
 	}
+	@RequestMapping("/sendMail")
+	@ResponseBody
+	public String sendMail(
+			String recipient,
+			String subject,
+			String body,
+			HttpServletResponse response)
+	{
+		try
+		{
+			/*
+			*/
+			sendMail(recipient, subject, body);
+			return "发送成功";
+		}
+		catch(Exception ex)
+		{
+			response.setStatus(400);
+			ex.printStackTrace();
+			return ex.toString();
+		}
+	}
 
+	private void sendMail(
+			String recipient,
+			String subject,
+			String body) throws Exception
+	{
+		Properties props = System.getProperties();
+		props.put("mail.smtps.host", mailConfigFacade.getSMTPHost());
+		props.put("mail.smtps.auth","true");
+		props.put("mail.smtps.port",mailConfigFacade.getMailPort());
+		props.put("mail.smtps.socketFactory.fallback", "true");
+		props.put("mail.smtp.socketFactory.fallback", "true");
+        props.put("mail.smtp.starttls.enable", "true");
+        props.put("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
+
+		javax.mail.Session session = javax.mail.Session.getInstance(props, null);
+		Message msg = new MimeMessage(session);
+		msg.setFrom(new InternetAddress(mailConfigFacade.getFromAddress()));
+		msg.setRecipients(Message.RecipientType.TO,
+			InternetAddress.parse(recipient, false));
+		msg.setSubject(subject);
+		msg.setText(body);
+		msg.setHeader("X-Mailer", "CDS");
+		msg.setSentDate(new Date());
+		SMTPTransport t =
+			(SMTPTransport)session.getTransport("smtps");
+		t.connect(mailConfigFacade.getSMTPHost(), mailConfigFacade.getFromAddress(), mailConfigFacade.getPassword());
+		t.sendMessage(msg, msg.getAllRecipients());
+		t.close();
+	}
+
+	@RequestMapping("/getMailParams")
+	@ResponseBody
+	public String getMailParams(HttpServletResponse response)
+	{
+		try
+		{
+			return mailConfigFacade.getMailParams();
+		}
+		catch(Exception ex)
+		{
+			response.setStatus(500);
+			ex.printStackTrace();
+			return ex.toString();
+		}
+	}
+
+	@RequestMapping("/setMailParams")
+	@ResponseBody
+	public String setMailParams(
+		@RequestBody(required = true) String newParamsStr,
+		HttpServletResponse response)
+	{
+		try
+		{
+			JsonParser parser = new JsonParser();
+			JsonObject newParams = 
+				parser.parse(newParamsStr).getAsJsonObject();
+			mailConfigFacade.setSMTPHost(newParams.get("host").getAsString());
+			mailConfigFacade.setFromAddress(newParams.get("address").getAsString());
+			mailConfigFacade.setPassword(newParams.get("password").getAsString());
+			mailConfigFacade.setMailPort(newParams.get("port").getAsString());
+			response.setStatus(200);
+			return newParams.toString();
+		}
+		catch(Exception e)
+		{
+			e.printStackTrace();
+			response.setStatus(400);
+			return "请求参数错误";
+		}
+	}
+	/**
+	 * 门店合同到期邮件告警
+	 */
+	@RequestMapping("/sendContractExpiringWaringMail")
+	@ResponseBody
+	public String sendContractExpiringWaringMail(
+		HttpServletResponse response)
+	{
+		try
+		{
+			List<PageData> floorDescList = mdFloorService.listFloorDesc();
+			Map<String, JsonObject> warningList = new HashMap();
+			for(PageData desc: floorDescList)
+			{
+				String floorId          = desc.getStringSafe("FLOORID");
+				String mallId           = desc.getStringSafe("FLOORID");
+				String floorDesc        = desc.getStringSafe("FLOORDESC");
+				PageData query          = new PageData();
+				SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
+				query.put("FLOORID", floorId);
+				query.put("contratMaturityDay", "1");
+				query.put("contratMaturityDay1", mailConfigFacade.getThreshhold(mallId));
+				query.put("DATADATE", format.format(format.parse(DateUtil.sdfDay.format(new Date()))));
+				query.put("BOOTHTYPECODE", "T1");
+				List<PageData> boothList = 
+					(List<PageData>)contratMaturityDayFacade
+						.getContratMaturityDayList(query)
+						.get("resultList");
+				if (boothList != null && boothList.size() > 0)
+				{
+					JsonObject mail = null;
+					if (warningList.containsKey(mallId) == false)
+					{
+						mail = new JsonObject();
+						mail.add("recipients", mailConfigFacade.listRecipients(mallId));
+						mail.addProperty("floors", "");
+						mail.addProperty("mallId", mallId);
+						warningList.put(mallId, mail);
+					}
+					else
+					{
+						mail = warningList.get(mallId);
+					}
+					String floors = mail.get("floors").getAsString();
+					floors += "\t " + floorDesc + "\n";
+				}
+			}
+			for (JsonObject mail: warningList.values())
+			{
+				JsonArray recipients = mail.get("recipients").getAsJsonArray();
+				for (JsonElement elem: recipients)
+				{
+					JsonObject recipient = elem.getAsJsonObject();
+					String name = recipient.get("name").getAsString();
+					String mallId = mail.get("mallId").getAsString();
+					String body = name + ", 您好:\n"
+						+ "\t下述楼层中, 存在将在" + mailConfigFacade.getThreshhold(mallId).toString() + "天内合同到期的柜位， 请您及时登录系统查看。\n"
+						+ mail.get("floors").getAsString()
+						+ "谢谢\n"
+						+ "CDS邮件提醒\n";
+					String address = recipient.get("address").getAsString();
+					sendMail(
+						address,
+						"正柜合同到期预警",
+						body);
+				}
+			}
+			return "发送成功";
+		}
+		catch(Exception e)
+		{
+			response.setStatus(400);
+			return "参数错误";
+		}
+	}
+
 }
Index: gervs-ws-client/.classpath
===================================================================
--- gervs-ws-client/.classpath	(revision 4194)
+++ gervs-ws-client/.classpath	(working copy)
@@ -1,37 +1,36 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.nondependency" value=""/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: gervs-ws-server/.classpath
===================================================================
--- gervs-ws-server/.classpath	(revision 4194)
+++ gervs-ws-server/.classpath	(working copy)
@@ -1,37 +1,36 @@
-<?xml version="1.0" encoding="UTF-8"?>
-<classpath>
-	<classpathentry kind="src" output="target/classes" path="src/main/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
-		<attributes>
-			<attribute name="optional" value="true"/>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-			<attribute name="org.eclipse.jst.component.nondependency" value=""/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
-		<attributes>
-			<attribute name="maven.pomderived" value="true"/>
-		</attributes>
-	</classpathentry>
-	<classpathentry kind="output" path="target/classes"/>
-</classpath>
+<?xml version="1.0" encoding="UTF-8"?>
+<classpath>
+	<classpathentry kind="src" output="target/classes" path="src/main/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="src" output="target/test-classes" path="src/test/java">
+		<attributes>
+			<attribute name="optional" value="true"/>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry excluding="**" kind="src" output="target/test-classes" path="src/test/resources">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.m2e.MAVEN2_CLASSPATH_CONTAINER">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
+		<attributes>
+			<attribute name="maven.pomderived" value="true"/>
+		</attributes>
+	</classpathentry>
+	<classpathentry kind="output" path="target/classes"/>
+</classpath>
Index: pom.xml
===================================================================
--- pom.xml	(revision 4194)
+++ pom.xml	(working copy)
@@ -384,7 +384,7 @@
 			<dependency>
 				<groupId>javax.mail</groupId>
 				<artifactId>mail</artifactId>
-				<version>1.4.7</version>
+				<version>1.4</version>
 			</dependency>
 			<!-- JEE websocket -->
 			<dependency>
@@ -676,11 +676,13 @@
 				<artifactId>gervs-ws-client</artifactId>
 				<version>${project.version}</version>
 			</dependency>
+			<!--
 			<dependency>
 				<groupId>com.gervs</groupId>
 				<artifactId>gervs-cache</artifactId>
 				<version>${project.version}</version>
 			</dependency>
+			-->
 			<dependency>
 				<groupId>com.gervs</groupId>
 				<artifactId>gervs-util</artifactId>
@@ -745,4 +747,4 @@
 		</profile>
 	</profiles>
 
-</project>
\ No newline at end of file
+</project>"""
    parser = Parser()
    dir(parser)
    theContent = '\n'.join(content.split('\n')[0:1]) + '\n'
    theContent = '\n'.join(content.split('\n')[85 :86]) + '\n'
    theContent = '\n'.join(content.split('\n')[78 :107]) + '\n'
    theContent = '\n'.join(content.split('\n')[ :107]) + '\n'
    theContent = content.encode('utf-8')
    parser.parse(theContent)
    ret = parser.ret
    for path, diff in ret:
        print path[0][len('Index: '):-1]
        print diff
    quit()
    import re
    p = re.compile(ur"^ +[^\n]*")
    theLine = content.split('\n')[85 :86][0]
    print theLine
    m = p.match(theLine)
    print m
    quit()
