from _solve import Board, Block, Solve
from _test_maps import *
import unittest



class Test_Board(unittest.TestCase):
	def test_parsingBoardFromMatrix(self):
		board = Board._parseMatrix(Board1_4x4)

		for y in range(len(Board1_4x4)):
			for x in range(len(Board1_4x4[y])):
				block = board[x, y]
				self.assertEqual(
					block.Value,
					Board1_4x4[y][x][0],
					"Block with coordinates x: {}, y: {} should have value equal '{}' got '{}'".format(
						x,
						y,
						Board1_4x4[y][x][0],
						block.Value
					)
				)

				self.assertEqual(
					block.Direction,
					Board1_4x4[y][x][1],
					"Block with coordinates x: {}, y: {} should have direction equal '{}' got '{}'".format(
						x,
						y,
						Board1_4x4[y][x][1],
						block.Direction
					)
				)

class Test_SolveMethods(unittest.TestCase):
	def getMapOfBlocksNotLinking(self, solution, ways: list = []):
		solver = Solve(Board.parse(TestLinks1))
		solver.Ways = ways

		linkingMap = solver.getMapOfBlocksNotLinking()
		for y in range(len(linkingMap)):
			for x in range(len(linkingMap[0])):
				self.assertEqual(
					linkingMap[y][x],
					solution[y][x],
					"Block on x:{} and y:{} is {}".format(
						x,
						y,
						"not linking" if solution[y][x] else "linking"
					)
				)

	def test_getMapOfBlocksNotLinking_noWays(self):
		self.getMapOfBlocksNotLinking(TestLinks1_NotLinking)

	def test_getMapOfBlocksNotLinking_withWays(self):
		ways = [
			[(2, 0), (2, 1), (1, 2)],
			[(2, 3), (3, 2)]
		]
		solution = [ list(x) for x in list(TestLinks1_NotLinking).copy() ]
		for x, y in ((2, 0), (2, 1), (2, 3)):
			solution[y][x] = False

		self.getMapOfBlocksNotLinking(solution, ways)

	def getMapOfBlocksNotLinked(self, solution, ways: list = []):
		solver = Solve(Board.parse(TestLinks1))
		solver.Ways = ways

		linkingMap = solver.getMapOfBlocksNotLinked()
		for y in range(len(linkingMap)):
			for x in range(len(linkingMap[0])):
				self.assertEqual(
					linkingMap[y][x],
					solution[y][x],
					"Block on x:{} and y:{} is {}".format(
						x,
						y,
						"not linked" if solution[y][x] else "linked"
					)
				)

	def test_getMapOfBlocksNotLinked_withWays(self):
		ways = [
			[(2, 0), (2, 1), (1, 2)],
			[(2, 3), (3, 2)]
		]
		solution = [ list(x) for x in list(TestLinks1_NotLinked).copy() ]
		for x, y in ((2, 1), (1, 2), (3, 2)):
			solution[y][x] = False
		self.getMapOfBlocksNotLinked(solution, ways)

	def test_getMapOfBlocksNotLinked_noWays(self):
		self.getMapOfBlocksNotLinked(TestLinks1_NotLinked)

	def test_getAllBlocksOnWay(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)

		dataSet = (
			({board[2, 1], board[2, 0]}, (2, 2), "TOP"),
			({board[2, 3]}, (2, 2), "BOTTOM"),
			({board[2, 1], board[3, 1]}, (1, 1), "RIGHT"),
			({board[0, 1]}, (1, 1), "LEFT"),
			({board[2, 2], board[3, 1]}, (1, 3), "TOP_RIGHT"),
			({board[1, 1], board[2, 2], board[3, 3]}, (0, 0), "BOTTOM_RIGHT"),
			({board[1, 2], board[0, 3]}, (2, 1), "BOTTOM_LEFT"),
			({board[1, 2], board[0, 1]}, (2, 3), "TOP_LEFT")
		)

		for data in dataSet:
			self.assertEqual(
				set(solver.getAllBlocksOnWay(
					getattr(Block, "DIRECTION_"+data[2]),
					data[1]
				)),
				data[0],
				"Test getAllBlocksOnWay with way: {} and starting point: x={}, y={}".format(
					" and ".join(x[0].upper()+x[1:].lower() for x in str(data[2]).split("_")),
					*data[1]
				)
			)

	def test_checkOnlyOneMove_noWays(self):
		board = Board.parse(TestLinks1)
		self.assertEqual(
			sorted(tuple( tuple(line) for line in Solve(board).checkOnlyOneMove() )),
			sorted((
				((0,1), (0,2)),
				((2,3), (3,2)),
				((2,1), (0,1)),
				((3,1), (1,3)),
				((1,3), (1,2)),
				((2,2), (2,3))
			))
		)

	def test_checkOnlyOneMove_withWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		solver.Ways = [
			[(2,1), (0,1), (0,2)],
			[(3,1), (1,3)]
		]
		solver.checkOnlyOneMove()
		self.assertEqual(
			sorted(tuple( tuple(line) for line in solver.checkOnlyOneMove() )),
			sorted((
				((2,3), (3,2)),
				((1,3), (1,2)),
				((2,2), (2,3))
			))
		)

	def test_checkOnlyOneLinking_noWays(self):
		board = Board.parse(TestLinks1)
		self.assertEqual(
			sorted(tuple( tuple(line) for line in Solve(board).checkOnlyOneLinking() )),
			sorted((
				((2,1), (0,1)),
				((0,1), (0,2)),
				((0,2), (2,2)),
				((3,2), (3,1)),
				((3,1), (1,3))
			))
		)

	def test_checkOnlyOneLinking_withWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		solver.Ways = [
			[(1,3), (1,2), (3,0)],
			[(2,2), (2,3)],
		]
		self.assertEqual(
			sorted(tuple( tuple(line) for line in solver.checkOnlyOneLinking() )),
			sorted((
				((2,0), (2,1)),
				((2,1), (0,1)),
				((0,1), (0,2)),
				((0,2), (2,2)),
				((3,2), (3,1)),
				((3,1), (1,3)),
			))
		)

	def test_commitWay(self):
		board = Board.parse(TestLinks1)
		solver = Solve(Board.parse(TestLinks1))
		solver.Ways = [
			[(2,0), (2,1), (0,1)],
			[(2,3), (3,2), (3,1)],
		]
		solver.commitWay(solver.Ways[0])
		solver.commitWay(solver.Ways[1])
		board._map[1][2].Value = 5
		board._map[3][2].Value = 9
		board._map[2][3].Value = 10

		self.assertEqual(
			solver.Board.getValuesMatrix(),
			board.getValuesMatrix()
		)

	def test_addConnectionPointsToWays_noWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		points = [ # No logic connection, it's only ways
			[(1,2), (2,3)],
			[(0,1), (3,1)],
			[(3,1), (1,2)]
		]
		solver.addConnectionPointsToWays(points)
		self.assertEqual(
			solver.Ways,
			[
				[(0,1), (3,1), (1,2), (2,3)]
			]
		)

	def test_addConnectionPointsToWays_withWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		points = [
			[(1,2), (1,1)],
			[(0,1), (2,2)],
			[(3,3), (2,0)],
		]
		solver.Ways = [
			[(1,3), (2,3), (1,0), (0,1)],
			[(3,0), (3,1), (3,2), (3,3)]
		]
		solver.addConnectionPointsToWays(points)
		self.assertEqual(
			solver.Ways,
			[
				[(1,3), (2,3), (1,0), (0,1), (2,2)],
				[(3,0), (3,1), (3,2), (3,3), (2,0)],
				[(1,2), (1,1)]
			]
		)

	def test_checkOneBlockOnWay(self):
		board = Board.parse("5x5:1hda12ea14abegaac20a6daa4aafaaaac16a")
		self.assertEqual(
			sorted(tuple(tuple(line) for line in Solve(board).checkOneBlockOnWay() )),
			sorted((
				((3,0), (3,1)),
				((3,1), (0,1))
			))
		)

	def test_solve(self):
		dataSet = [
			# ( MAP, SOLUTION )
			(Board1_4x4, Solution1_4x4),
			(Board2_4x4, Solution2_4x4),
			(
				"5x5:ed18dcfdaeceach1g25acfaag8aa22gbg",
				Board.parse("5x5:3e15d18d11c12f4d14a16e19c20e2a24c13h1g25a9c7f17a10a6g8a23a22g5b21g").getValuesMatrix()
			),
			(
				"7x7:1dfcdfegd26efg30dfedfbdbf45edad2gfaae38baaaha18bcd5hghebca33g12ag49a",
				Board.parse("7x7:1d8f15c43d16f19e14g9d26e35f25g30d21f47e6d36f24b39d13b31f45e37d7a3d2g41f20a44a17e38b23a42a29a40h46a18b27c32d5h4g28h48e22b11c34a33g12a10g49a").getValuesMatrix()
			),
			(
				"7x7:1d26cege27egda15eecgge46cddd22h11eaebecbhcdbba5eg37c39agd20hdga41ca42ghh49a",
				Board.parse("7x7:1d26c14e13g19e27e18g45d25a15e29e23c28g24g33e46c47d8d3d22h11e44a40e7b30e9c10b12h34c35d17b21b2a5e4g37c39a36g31d20h48d38g43a41c16a42g32h6h49a").getValuesMatrix()
			),
			(
				"7x7:1cd40dced35gda7eh14ggg47ecdadcgcbafehhdhgdge41gda18b21eaggcabb20ha49a",
				Board.parse("7x7:1c16d40d34c36e2d35g5d15a7e39h14g4g3g47e32c29d33a37d45c46g43c28b6a30f19e38h44h9d42h8g12d11g23e41g26d31a18b21e13a25g17g48c27a10b22b20h24a49a").getValuesMatrix()
			),
			(
				"12x12:51ddfeccdc108egf1fee85e132d117dagc144a7d95ef126ea14c81d110a18g59ed113g16efg50adc122cgg118e71e77gff44fc88c99cgf47c119fdh87gaf30c31cca42h120ad124h104afh32f93c21eh39dbb52fchh92gf127cca11g128ed140dd83hf56bg61bbchg40hgcb82hf142fc70bgcfah37eh134h96g54aa22a9daac4ghah74ggahbac35aa72c143aaag",
				Board.parse("12x12:51d84d125f131e111c107c112d25c108e24g26f1f66e20e85e132d117d106a116g62c144a7d95e63f126e19a14c81d110a18g59e114d113g16e8f15g50a79d43c122c78g121g118e71e77g123f90f44f102c88c99c98g100f47c119f103d105h87g89a48f30c31c41c80a42h120a2d124h104a45f115h32f93c21e101h39d6b94b52f91c109h17h92g57f127c12c13a11g128e36d140d135d83h34f56b55g61b23b27c29h28g40h60g141c33b82h133f142f68c70b69g53c129f46a49h37e97h134h96g54a65a22a9d130a5a75c4g38h76a139h74g3g67a64h86b10a137c35a58a72c143a138a73a136g").getValuesMatrix()
			),
			(
				"25x25:409dde533fec515ee324eefed540ge382ed468fg381g54d58e117f116gg68e139c179c140e459dgd317dhe321c180d322eegg328c329dg594fd292f192e364e291g392ce488e538bege476cc495ba201c2d205ce217f390g380b189ehceef203f126e560b491dc563d567e460ddc612e351gc400e347eee159ege118g307fegh268fe625a523eb410e254f473g44d177hd318e166ch167chde168a190de20fega55e110d226dc143df236c333e582cb237ca583e131c608e79e238eehf526f415gdca225g47d535e150d412d472bdd200b62d45c263g420he529e46g239heg8gg525hgcf61g575d198a34e65c215d345c10fc512c63ccbf530e78aa214g346h207d542ff66h193efg69ceca278ce27ce279e550a228f70c71c531ge277g72d49e600cb28g233fa249e339e255dc489a432e441e76b404e18bdge387bf314d313g446d211fgb266g208gbh250f248h573e465e35c433de620eg36ece32fb590f461c259f156f464g571c407e258g3e89fa462fgb466c256cac586ef227b506eh304cg1a527eh315ffa377f385hh181f305fg302g574ac299d430ac569d229f98e579a104d589b497fd549hec298geb384a121cb548ge246g127ebbg218ce403a188b109h293b623d450efa81e622ga219a355d182fag164a372eg596c51c521e274e230ca595ga108a242d260b157a359d184fbh231dg183ga52ed273g113ea399bcc396g395g288ce37b576d21f336ca269a360f394g137dd173cg175d5fah365f174ga617c522a142a153b619a405e498c508b613e310c185f448h234f311e455f222bag309ga499e447g114ea102d197a505bb481d568a554f99c507a552c434a480g195ch624hc463ag354ae101gc194g479g196gc443aa437f442gc519f357dg241agf556f243bd216ah374h408h369e53a545ea356g611h128d282c103bdbg290baa615egc453c609c30faa558h146h366e283c232af176hac271c149a275b7bggah494aac485c528a457a6g272b112bd342ghff115agcca141a439eb95fh578a91c90gc484ach161cbd252c162b414a487h253hg92g588b536caaag406b376b280hcf483b547b348ba136a160ha85g286hf546g138hfad445bccab502g17a504haa605caa82aa133c501g134g367a413ag606ga245a22cc524bh361b235a25ab87g616h24g451b371bh300b171b389a570aag4ah344h373h23g",
				Board.parse("25x25:409d199d490e533f561e539c515e581e324e240e471f496e541d540g77e382e19d468f514g381g54d58e117f116g57g68e139c179c140e459d178g475d317d580h551e321c180d322e39e458g67g328c329d327g594f565d292f192e364e291g392c534e488e538b562e391g26e476c325c495b320a201c2d205c393e217f390g380b189e326h202c477e423e206f203f126e560b491d352c563d567e460d119d421c612e351g158c400e347e469e170e159e169g353e118g307f261e566g422h268f41e625a523e474b410e254f473g44d177h417d318e166c323h167c470h295d388e168a190d308e20f59e165g363a55e110d226d130c143d411f236c333e582c416b237c319a583e131c608e79e238e132e38h425f526f415g338d224c362a225g47d535e150d412d472b9d264d200b62d45c263g420h401e529e46g239h221e220g8g419g525h262g330c331f61g575d198a34e65c215d345c10f511c512c63c213c513b402f530e78a294a214g346h207d542f602f66h193e13f64g69c444e48c532a278c287e27c375e279e550a228f70c71c531g29e277g72d49e600c601b28g233f191a249e339e255d210c489a432e441e76b404e18b492d209g435e387b270f314d313g446d211f386g267b266g208g60b424h250f248h573e465e35c433d152e620e151g36e155c493e32f564b590f461c259f156f464g571c407e258g3e89f223a462f572g43b466c256c431a585c586e334f227b506e154h304c584g1a527e212h315f106f467a377f385h257h181f305f303g302g574a11c299d430a97c569d229f98e579a104d589b497f509d549h80e383c298g378e12b384a121c247b548g122e246g127e75b429b74g218c598e403a188b109h293b623d450e147f204a81e622g297a219a355d182f306a73g164a372e296g596c51c521e274e230c597a595g187a108a242d260b157a359d184f265b332h231d50g183g418a52e349d273g113e301a399b397c335c396g395g288c289e37b576d21f336c449a269a360f394g137d244d173c398g175d5f337a350h365f174g42a617c522a142a153b619a405e498c508b613e310c185f448h234f311e455f222b379a618g309g120a499e447g114e56a102d197a505b593b481d568a554f99c507a552c434a480g195c40h624h100c463a553g354a368e101g478c194g479g196g544c443a33a437f442g555c519f357d543g241a436g577f556f243b83d216a559h374h408h369e53a545e163a356g611h128d282c103b16d276b281g290b316a107a615e15g557c453c609c30f454a105a558h146h366e283c232a284f176h610a517c271c149a275b7b148g516g186a518h494a14a456c485c528a457a6g272b112b343d342g510h285f486f115a341g438c591c129a141a439e599b95f592h578a91c90g251c484a93c452h161c111b84d252c162b414a487h253h94g92g588b536c520a537a440a587g406b376b280h482c86f483b547b348b312a136a160h172a85g286h144f546g138h124f340a426d445b604c503c96a621b502g17a504h614a31a605c358a607a82a135a133c501g134g367a413a500g606g123a245a22c427c524b603h361b235a25a88b87g616h24g451b371b428h300b171b389a570a145a370g4a125h344h373h23g").getValuesMatrix()
			),
			(
				"30x30:e779e449c39cc563e61e757cc309e535c134c450ef840f839g40eg135f320d536ecdf497fg758f395ef38g424de106dd488d526c57e642d292e514cee119eeeeg202e527e674f438gg702f220gb219gf793fc897f676d781d850de138dda190c629e66e764c795e120ed479f478g193d765d543e192g380c443fg65gc256e300f379gg382e314d385d174e84c247e162dc525hfd632ccfe722e440c41e232f313gd537f498e595fd96g868ef441b126fgc613e206e425e289d710d160d731d283d322e600eed91h457che204g599gf681hcaged456g397e458gfd78cc699d239c502d10d241eb323cb796e279f278gf804d393b324dfcf361fg114e267g240g276ga79e360g589c614cbc677c1e156e679ce310e678g477b615cb616e695fd703ebc806ef542h306ae153c245bgggc777ee698a593ccah332ec555c553g117e643f436f743d716a591c594b746e556cef338f592g432f99f619b463e462g798e551h49de104cd566a550gc105h136dchb491c742a852ec217f899e301cf898gc302g152a48g659f705f492eb418c845g169c860d43d809ee561b171c836efg45c516c46ec859g144fe808g517f421e788f761e419g275af80fgc417a33e800b123f564ca888e686c32ge8d689cacf690g825d540d688g805ae325fdg824ge272e431h887ga602d494a841d215d775d810eec131c601g83h444f165df180f453eh82g745a334f773c132h196hhe81g195ggg344ea448ag480e709aehcf712dda711g884e838a662d203adf141f558f661g63e465e818f194b766f504f264edb336cf653cc408ca331ab652g286h725b179bh792b854c663fhf751f858h660aafef750gf409f187ccd280c646d364d469e756aca93c768e281a95b878f16d339ega189h295c826ea94g297c637f298e483e294gg634ce34cd249e579d532d730a630acbb236bd266bg128g262ee900a35da819f531g624df299a635h430age778ae407b214a363a159a445df67e181fb403f70b386f546ha11hh823bb372d545ga763h257d26eb464h101feb18bc250d355a329cch234a837ba330hd833e142b29d577hg399af499ebg762a530h27g398gh359ab177c644g697a225dd328a692d871ecga121da261bab549hbe610e671af115hf869g735fa609gh88c738e413dcd226cb341d452b877bah451ge55c47b508d700cf501hdg701a524h56hgg744h90haa435b207c538c210bf58a753eh69bdc401ehf521eha130h173hbe523bh76f373ha378a539hf584cb741b212aca811cb585c667e651a581h533hg507b588h367c587g586g368ch369e422g883h487h813f4afe812gbb412a596f346e148e158abc311cg559c665b111c260ac776h467aa112a410c560h573h53f161hg108d821fh110g348c327b849adf253ge388f872chg342hd706a733c786b638h122hh570c873e734b572a814h349ceh284eg167faafcbd387b881cg68ah476ae783c185g446h785hb529bbh670a270c782g486a427gh271a784g36e727a176a147be248a831c657bg229c209h352c222b656g353h885b603c365b230a216a736bh828hh604f623a351g107af357da345bahc771cg73c752a576b513a575g769g224h74c506aa853a22hb102c611g772ahc685h316a274a7h163hab867b894fbh326h606c754a415acga402a198ccb454g893g714a748h807ag269aa669h713g548hae166ac304bc880b51c472ag242bca184b767a511gbbc340h52bh390bcd50g861h622a509a684h484a608aab518c335a13b151bc62bc519c31a474c475a856a649ca520a890h648g650hgcahh466hg875a285h30g383h",
				Board.parse("30x30:87e779e449c39c865c563e61e757c496c309e535c134c450e801f840f839g40e562g135f320d536e394c461d307f497f864g758f395e866f38g424d384e106d164d488d526c57e642d292e514c92e221e119e197e515e439e291g202e527e674f438g673g702f220g863b219g237f793f896c897f676d781d850d12e138d356d60a190c629e66e764c795e120e721d479f478g193d765d543e192g380c443f191g65g381c256e300f379g442g382e314d385d174e84c247e162d567c525h85f97d632c125c633f568e722e440c41e232f313g682d537f498e595f759d96g868e305f441b126f246g205c613e206e425e289d710d160d731d283d322e600e375e857d91h457c133h717e204g599g740f681h459c460a321g760e317d456g397e458g228f268d78c277c699d239c502d10d241e631b323c374b796e279f278g835f804d393b324d715f113c726f361f238g114e267g240g276g396a79e360g589c614c495b155c677c1e156e679c139e310e678g477b615c319b616e695f590d703e680b244c806e146f542h306a621e153c245b318g620g154g552c777e847e698a593c287c59a288h332e554c555c553g117e643f436f743d716a591c594b746e556c557e71f338f592g432f99f619b463e462g798e551h49d20e104c802d566a550g851c105h136d490c282h437b491c742a852e704c217f899e301c303f898g658c302g152a48g659f705f492e846b418c845g169c860d43d809e755e561b171c836e640f170g45c516c46e420c859g144f172e808g517f421e788f761e419g275a259f80f787g799c417a33e800b123f564c565a888e686c32g574e8d689c720a687c691f690g825d540d688g805a371e325f100d719g824g683e272e431h887g86a602d494a841d215d775d810e829e333c131c601g83h444f165d723f180f453e628h82g745a334f773c132h196h243h817e81g195g774g493g344e780a448a447g480e709a157e19h140c696f712d547d118a711g884e838a662d203a544d127f141f558f661g63e465e818f194b766f504f264e406d124b336c582f653c749c408c641a331a44b652g286h725b179b9h792b854c663f116h400f751f858h660a337a654f636e5f750g855f409f187c188c354d280c646d364d469e756a293c308a93c768e281a95b878f16d339e468g143a189h295c826e541a94g297c637f298e483e294g296g634c434e34c213d249e579d532d730a630a235c862b218b236b129d266b578g128g262e528e900a35d672a819f531g624d510f299a635h430a265g583e778a848e407b214a363a159a445d211f67e181f145b403f70b386f546h290a11h137h823b816b372d545g64a763h257d26e429b464h101f728e201b18b233c250d355a329c28c416h234a837b794a330h569d833e142b29d577h17g399a732f499e886b200g762a530h27g398g392h359a645b177c644g697a225d251d328a692d871e23c870g639a121d178a261b803a718b549h815b747e610e671a505f115h24f869g735f258a609g391h88c738e413d89c481d226c724b341d452b877b534a797h451g707e55c47b508d700c655f501h6d500g701a524h56h737g876g744h90h227a675a435b207c538c210b2f58a753e343h69b580d377c401e708h208f521e42h231a130h173h503b827e523b489h76f373h98a378a539h625f584c598b741b212a3c362a811c791b585c667e651a581h533h666g507b588h367c587g586g368c423h369e422g883h487h813f4a485f626e812g729b739b412a596f346e148e158a15b664c311c14g559c665b111c260a820c776h467a312a112a410c560h573h53f161h411g108d821f627h110g348c327b849a182d254f253g72e388f872c433h252g342h693d706a733c786b638h122h366h570c873e734b572a814h349c350e822h284e571g167f405a597a175f426c790b473d387b881c789g68a186h476a223e783c185g446h785h263b529b428b77h670a270c782g486a427g882h271a784g36e727a176a147b879e248a831c657b830g229c209h352c222b656g353h885b603c365b230a216a736b54h828h832h604f623a351g107a273f357d109a345b612a404h21c771c770g73c752a576b513a575g769g224h74c506a694a853a22h75b102c611g772a103h315c685h316a274a7h163h358a255b867b894f455b347h326h606c754a415a668c414g376a402a198c617c522b454g893g714a748h807a605g269a199a669h713g548h618a607e166a471c304b389c880b51c472a470g242b183c512a184b767a511g482b25b891c340h52b892h390b842c843d50g861h622a509a684h484a608a37a895b518c335a13b151b149c62b889c519c31a474c475a856a649c834a520a890h648g650h647g874c370a844h168h466h150g875a285h30g383h").getValuesMatrix()
			),
			(Board3_16x16, Solution3_16x16),
			(BoardI, SolutionI)
		]

		for data in dataSet:
			solution = Solve(Board.parse(data[0])).solve()
			for y in range(len(data[1])):
				for x in range(len(data[1][y])):
					self.assertEqual(
						solution[y][x],
						data[1][y][x]
					)

if __name__ == "__main__":
	unittest.main()
