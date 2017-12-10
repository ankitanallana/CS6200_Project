package hw4;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
	private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	public static void main(String[] args) throws IOException {
		System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String s = br.readLine();

		HW4 indexer = null;
		try {
			indexLocation = s;
			indexer = new HW4(s);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		// ===================================================
		// read input from user until he enters q for quit
		// ===================================================
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out
				.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
				System.out
				.println("[Acceptable file types: .xml, .html, .html, .txt]");
				s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}
				// try to add file into the index
				indexer.indexFileOrDirectory(s);
			} catch (Exception e) {
				System.out.println("Error indexing " + s + " : "
						+ e.getMessage());
			}
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
				indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);
		s = "";
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out.println("press enter");
				s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}
				
			
				String[] queryArray = {"what articles exist which deal with tss time sharing system an operating system for ibm computers","i am interested in articles written either by prieve or udo pooch prieve b pooch u","intermediate languages used in construction of multi-targeted compilers tcoll","im interested in mechanisms for communicating between disjoint processes possibly but not exclusively in a distributed environmenti would rather see descriptions of complete mechanisms with or without implementations as opposed to theoretical work on the abstract problemremote procedure calls and message-passing are examples of my interests","id like papers on design and implementation of editing interfaces window-managers command interpreters etcthe essential issues are human interface design with views on improvements to user efficiency effectiveness and satisfaction","interested in articles on robotics motion planning particularly the geometric and combinatorial aspectswe are not interested in the dynamics of arm motion","i am interested in distributed algorithms - concurrent programs in which processes communicate and synchronize by using message passing areas of particular interest include fault-tolerance and techniques for understanding the correctness of these algorithms","addressing schemes for resources in networks resource addressing in network operating systems","security considerations in local networks network operating systems and distributed systems","parallel languages languages for parallel computation","setl very high level languages","portable operating systems","code optimization for space efficiency","find all discussions of optimal implementations of sort algorithms for database management applications","find all discussions of horizontal microcode optimization with special emphasis on optimization of loops and global optimization","find all descriptions of file handling in operating systems based on multiple processes and message passing","optimization of intermediate and machine code","languages and compilers for parallel processors especially highly horizontal microcoded machines code compaction","parallel algorithms","graph theoretic algorithms applicable to sparse matrices","computational complexity intractability class-complete reductions algorithms and efficiency","i am interested in hidden-line and hidden-surface algorithms for cylinders toroids spheres and conesthis is a rather specialized topic in computer graphics","distributed computing structures and algorithms","applied stochastic processes","performance evaluation and modelling of computer systems","concurrency control mechanisms in operating systems","memory management aspects of operating systems","any information on packet radio networksof particular interest are algorithms for packet routing and for dealing with changes in network topographyi am not interested in the hardware used in the network","number-theoretic algorithms especially involving prime number series sieves and chinese remainder theorem","articles on text formatting systems including what you see is what you get systemsexamples"
						+ " off scribe bravo","id like to find articles describing the use of singular value decomposition in digital image processingapplications include finding approximations to the original image and restoring images that are subject to noise an article on the subject is h andrews and c patterson outer product expansions and their uses in digital image processing american mathematical andrews h patterson c","id like to find articles describing graph algorithms that are based on the eigenvalue decomposition or singular value decomposition of the ajacency matrix for the graphim especially interested in any heuristic algorithms for graph coloring and graph isomorphism using this method","articles about the sensitivity of the eigenvalue decomposition of real matrices in particular zero-one matricesim especially interested in the separation of eigenspaces corresponding to distinct eigenvalues articles on the subject c davis and w kahn the rotation of eigenvectors by a permutation siam j numerical analysis vol 7 no 1 1970 g stewart error bounds for approximate invariant subspaces of closed linear operators siam j numerical analysis vol 8 no 4 1971 davis c kahn w stewart g","currently interested in isolation of root of polynomial there is an old more recent material heindel l","probabilistic algorithms especially those dealing with algebraic and symbolic manipulationsome examples rabiin probabilistic algorithm on finite field siam waztch probabilistic testing of polynomial identities siam rabinm","fast algorithm for context-free language recognition or parsing","articles describing the relationship between data types and concurrency eg what is the type of a processwhen is a synchronization attemptbetween two processes type correctin a message-passing system is there any notion of the types of messages--ie any way to check that the sender of the message and the receiver are both treating the bit stream as some particular type","what is the type of a module	i dont want the entire literature on abstract data types here but im not sure how to phrase this to avoid it im interested in questions about how one can check that a module matches contexts in which it is used","what does type compatibility mean in languages that allow programmer defined typesyou might want to restrict this to extensible languages that allow definition of abstract data types or programmer-supplied definitions of operators like ","list all articles dealing with data types in the following languages that are referenced frequently in papers on the above languages eg catch any languages with interesting type structures that i might have missed","theory of distributed systems and databasessubtopics of special interest include reliability and fault-tolerance in distributed systems atomicity distributed transactions synchronization algorithmsresource allocation lower bounds and models for asynchronous parallel systemsalso theory of communicating processes and protocols p box 2158 yale station new haven conn06520","computer performance evaluation techniques using pattern recognition and clusteringla70803","analysis and perception of shape by humans and computersshape descriptions shape recognition by computertwo-dimensional shapes measures of circularityshape matching","texture analysis by computer digitized texture analysistexture synthesis perception of texture","the use of operations research models to optimize information system performancethis includes fine tuning decisions such as secondary index selection file reorganization and distributed databases","the application of fuzzy subset theory to clustering and information retrieval problemsthis includes performance evaluation and automatic indexing considerations","the use of bayesian decision models to optimize information retrieval system performancethis includes stopping rules to determine when a user should cease scanning the output of a retrieval search","the use of computer science principles eg data structuresnumerical methods in generating optimization eg linear programming algorithmsthis includes issues of the khachian russian ellipsoidal algorithm and complexity of such algorithms","the role of information retrieval in knowledge based systems ie expert systems","parallel processors in information retrieval","parallel processors and paging algorithms","modelling and simulation in agricultural ecosystems","mathematical induction group theory integers modulo m probability binomial coefficients binomial theorem homomorphism morphism transitivity relations relation matrixsyracuse university 313 link hall syracuse n 13210","semantics of programming languages including abstract specifications of data types denotational semantics and proofs of correctness hoare a dijkstra euniversity of massachusetts amherst ma 01003","anything dealing with star height of regular languages or regular expressions or regular events","articles relation the algebraic theory of semigroups and monoids to the study of automata and regular languages","abstracts of articles j backus can programming be liberated from the von neumann stylea functional style and its algebra of programs cacm 21 re millo r lipton a perlis letter to acm forum cacm 22 	 1979 629-630 backus j de millo r lipton r perlis a","algorithms or statistical packages for anova regression using least squares or generalized linear modelssystem design capabilities statistical formula are of intereststudents t test wilcoxon and sign tests multivariate and univariate components can be included","dictionary construction and accessing methods for fast retrieval of words or lexical items or morphologically related information hashing or indexing methods are usually applied to english spelling or natural language problems","hardware and software relating to database management systems database packages back end computers special associative hardware with microcomputers attached to disk heads or things like raprelational or network codasyl or hierarchical models systems like system r ims adabas total etc","information retrieval articles by gerard salton or others about clustering bibliographic coupling use of citations or co-citations the vector space model boolean search methods using inverted files feedback etc salton g","results relating parallel complexity theory both for prams and uniform circuits","algorithms for parallel computation and especially comparisons between parallel and sequential algorithms","list all articles on el1 and ecl el1 may be given as el1 i dont remember how they did it"};	
				
				for (int z = 0;z<queryArray.length;z++){
					Query q = new QueryParser(Version.LUCENE_47, "contents",
							sAnalyzer).parse(queryArray[z]);
					TopDocs docs = searcher.search(q, 100);
					ScoreDoc[] hits = docs.scoreDocs;

					// 4. display results
					String temp = "";
					for (int i = 0; i < hits.length; ++i) {
						int docId = hits[i].doc;
						Document d = searcher.doc(docId);
						String hit = "" + hits[i].score + "       ";
						temp = temp  +  z + " Q0 " + i + " " + hit.substring(0,7) + " " + d.get("path").substring(27,36)
								+ " LUCENE_standard_lower_punc \n"  ;
					}
					write(temp, "QueryID:" + z);
				}
			} catch (Exception e) {
				System.out.println("Error searching " + s + " : "
						+ e.getMessage());
				break;
			}
			s = "q";
		}
		
	}

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	HW4(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
				sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),
						Field.Store.YES));
				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html")
					|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
	
    public static void write(String S , String name) {

        try {
            File newTextFile = new File(name);

            FileWriter fw = new FileWriter(newTextFile);
            fw.write(S);
            fw.close();

        } catch (IOException iox) {
            //do stuff with exception
            iox.printStackTrace();
        }
    }
    
}